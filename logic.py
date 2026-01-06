import os
import hashlib
import imagehash
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing

# Copyright (c) 2025 Photo Comparator. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff'}

# --- Top Check Functions (Must be picklable for Multiprocessing) ---
def process_file_hashes(args):
    """
    Worker function to calculate hashes for a single file.
    Args: (filepath, use_phash)
    Returns: (filepath, size, md5, phash)
    """
    filepath, use_phash = args
    if not os.path.exists(filepath):
        return None
    
    res_md5 = None
    res_phash = None
    file_size = 0
    
    try:
        file_size = os.path.getsize(filepath)
        
        # MD5
        md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(65536), b''):
                md5.update(block)
        res_md5 = md5.hexdigest()
        
        # PHash
        if use_phash:
            with Image.open(filepath) as img:
                res_phash = imagehash.phash(img)
                
    except Exception as e:
        # print(f"Error processing {filepath}: {e}")
        return None

    return (filepath, file_size, res_md5, res_phash)

class ImageScanner:
    def __init__(self, callback_progress=None):
        self.callback_progress = callback_progress
        self.stop_requested = False
        # Create a manager event for stopping child processes if needed, 
        # but pure pool shutdown is usually easier.

    def find_images(self, folder):
        """Recursively find all images in a folder."""
        images = []
        for root, _, files in os.walk(folder):
            for file in files:
                if self.stop_requested: return []
                if os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS:
                    images.append(os.path.join(root, file))
        return images

    def scan_folders_parallel(self, folder_list, use_phash=True, min_size=0, max_size=None):
        """
        Scan a LIST of folders using Multiprocessing.
        Returns a dict mapping filepath -> {'size': int, 'md5': str, 'phash': hash object}.
        """
        results = {}
        all_files = []
        
        # 1. Gather all files (Deduplicated)
        seen_files = set()
        for folder in folder_list:
            if self.stop_requested: return {}
            if os.path.isdir(folder):
                for f in self.find_images(folder):
                    if f not in seen_files:
                        all_files.append(f)
                        seen_files.add(f)
        
        # 2. Pre-filter by size (Quick check before hashing)
        tasks = []
        for f in all_files:
            if self.stop_requested: return {}
            try:
                size = os.path.getsize(f)
                if size < min_size:
                    continue
                if max_size is not None and size > max_size:
                    continue
                tasks.append((f, use_phash))
            except:
                continue
                
        total = len(tasks)
        if total == 0:
            return {}

        # 3. Process in Parallel
        # Use slightly less than max cores to keep UI responsive
        max_workers = max(1, multiprocessing.cpu_count() - 1)
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all
            futures = [executor.submit(process_file_hashes, task) for task in tasks]
            
            for i, future in enumerate(as_completed(futures)):
                if self.stop_requested:
                    executor.shutdown(wait=False, cancel_futures=True)
                    return {}
                    
                result = future.result()
                if result:
                    fpath, fsize, fmd5, fphash = result
                    results[fpath] = {
                        'path': fpath,
                        'size': fsize,
                        'md5': fmd5,
                        'phash': fphash
                    }
                
                if self.callback_progress:
                    # Update progress every few items to avoid flooding UI queue
                    if i % 5 == 0 or i == total - 1:
                        import languages
                        self.callback_progress(i + 1, total, languages.get_text("status_analyzing", i+1, total))

        return results

    def compare_folders(self, folders_a, folders_b, threshold=0.90, check_similar=True, min_size=0, max_size=None):
        """
        Optimized comparison.
        1. Exact Match: Group by FILE SIZE first. MD5 compare only if size matches.
           (Note: Since we already calculated MD5 for everything in scan phase, we can just map MD5->Files)
        2. Similar Match: Optimized N*N loop (TODO: BK-Tree overkill for now, but skipping exact matches helps)
        """
        # Scan A
        if self.callback_progress:
            import languages
            self.callback_progress(0, 0, languages.get_text("status_scanning_a"))
        data_a = self.scan_folders_parallel(folders_a, use_phash=check_similar, min_size=min_size, max_size=max_size)
        if self.stop_requested: return [], []

        # Scan B or Self
        self_compare = False
        if folders_b:
            if self.callback_progress:
                import languages
                self.callback_progress(0, 0, languages.get_text("status_scanning_b"))
            data_b = self.scan_folders_parallel(folders_b, use_phash=check_similar, min_size=min_size, max_size=max_size)
            if self.stop_requested: return [], []
            
            source_list = list(data_a.values())
            target_list = list(data_b.values())
        else:
            self_compare = True
            source_list = list(data_a.values())
            target_list = source_list
        
        matches = []
        matched_a_paths = set()
        
        # --- Comparison Logic ---
        
        # Strategy:
        # A. Find Exact Matches using Dictionary (O(N)) - Extremely Fast
        # Map: MD5 -> [List of Files in B]
        
        map_b_md5 = {}
        target_indices = range(len(target_list))
        
        # If self compare, we need careful indexing
        # Construct index for B
        if not self_compare:
            for img in target_list:
                if img['md5']:
                    if img['md5'] not in map_b_md5:
                        map_b_md5[img['md5']] = []
                    map_b_md5[img['md5']].append(img)

        total_comparisons = len(source_list) * len(target_list) if not self_compare else (len(source_list)**2)//2
        processed = 0
        
        # We will iterate through A
        for i, img1 in enumerate(source_list):
            if self.stop_requested: break
            
            # --- 1. Exact Match Check (Fast) ---
            found_exact = False
            if img1['md5']:
                if self_compare:
                    # Search rest of list
                    for j in range(i + 1, len(source_list)):
                        img2 = source_list[j]
                        if img1['md5'] == img2['md5']:
                            matches.append(self._make_match(img1, img2, "完全相同", 100.0))
                            matched_a_paths.add(img1['path'])
                            matched_a_paths.add(img2['path'])
                else:
                    # Look up in map
                    if img1['md5'] in map_b_md5:
                        for img2 in map_b_md5[img1['md5']]:
                            matches.append(self._make_match(img1, img2, "完全相同", 100.0))
                            matched_a_paths.add(img1['path'])
            
            # --- 2. Similarity Check (Slow, O(N*N)) ---
            # Only if requested AND (optionally skip if already exact match? Users might want both)
            # Users usually care about similarity if *not* exact. 
            # But let's check anyway or strictly follow mode.
            if check_similar and img1['phash']:
                # For self compare
                start_idx = i + 1 if self_compare else 0
                target_subset = source_list if self_compare else target_list
                
                # To speed up, we don't compare with self or exact matches again if possible?
                # Actually, phash check is independent.
                
                for j in range(start_idx, len(target_subset)):
                    if self_compare and i == j: continue # Should be covered by start_idx
                    
                    img2 = target_subset[j]
                    
                    # Optimization: If sizes are excessively different, visual similarity is unlikely to be high?
                    # Not necessarily true (resize).
                    
                    # Optimization: Skip if we already found an Exact Match between these two?
                    # We can't easily know if *this specific pair* was exact match without storing pairs.
                    if img1['md5'] == img2['md5']:
                        continue # Already captured as exact match (MD5 implies PHash sameness)

                    if img2['phash']:
                        score = self._calc_similarity(img1['phash'], img2['phash'])
                        if score >= (threshold * 100):
                            matches.append(self._make_match(img1, img2, "視覺相似", score))
                            matched_a_paths.add(img1['path'])
                            if self_compare:
                                matched_a_paths.add(img2['path'])

            # Rough progress update (batching)
            processed += len(target_list) if not self_compare else (len(source_list) - i)
            if i % 10 == 0 and self.callback_progress:
                import languages
                self.callback_progress(min(processed, total_comparisons), total_comparisons, languages.get_text("status_comparing", i, len(source_list)))
        
        if self.callback_progress:
            import languages
            self.callback_progress(total_comparisons, total_comparisons, languages.get_text("status_finished"))

        unique_in_a = [img['path'] for img in source_list if img['path'] not in matched_a_paths]
        return matches, unique_in_a

    def _make_match(self, img1, img2, mtype, score):
        return {
            'file_a': img1['path'],
            'file_b': img2['path'],
            'type': mtype,
            'score': round(score, 1)
        }

    def _calc_similarity(self, h1, h2):
        diff = h1 - h2
        # Normalized 0-100
        return max(0, (64 - diff) / 64) * 100
