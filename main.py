import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
import os
import logic
import languages

# Copyright (c) 2025 Photo Comparator. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

# Set default theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(languages.get_text("app_title"))
        self.geometry("1000x700")

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Sidebar (Controls) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="照片比對工具", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Folder A Group
        self.folder_a_label = ctk.CTkLabel(self.sidebar_frame, text="群組 A (來源):", anchor="w")
        self.folder_a_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.list_a = tk.Listbox(self.sidebar_frame, height=4, bg="#2b2b2b", fg="white", selectbackground="#1f538d", borderwidth=0)
        self.list_a.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_frame_a = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.btn_frame_a.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        
        self.add_a_btn = ctk.CTkButton(self.btn_frame_a, text="新增", width=60, command=lambda: self.add_folder(self.list_a))
        self.add_a_btn.pack(side="left", padx=(0,5))
        self.batch_a_btn = ctk.CTkButton(self.btn_frame_a, text="批次", width=60, fg_color="#555", command=lambda: self.batch_add_folder(self.list_a))
        self.batch_a_btn.pack(side="left", padx=(0,5))
        self.clear_a_btn = ctk.CTkButton(self.btn_frame_a, text="清空", width=60, fg_color="darkred", hover_color="#8b0000", command=lambda: self.list_a.delete(0, tk.END))
        self.clear_a_btn.pack(side="left")

        # Folder B Group
        self.folder_b_label = ctk.CTkLabel(self.sidebar_frame, text="群組 B (若空則自我比對):", anchor="w")
        self.folder_b_label.grid(row=4, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.list_b = tk.Listbox(self.sidebar_frame, height=4, bg="#2b2b2b", fg="white", selectbackground="#1f538d", borderwidth=0)
        self.list_b.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_frame_b = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.btn_frame_b.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        self.add_b_btn = ctk.CTkButton(self.btn_frame_b, text="新增", width=60, command=lambda: self.add_folder(self.list_b))
        self.add_b_btn.pack(side="left", padx=(0,5))
        self.batch_b_btn = ctk.CTkButton(self.btn_frame_b, text="批次", width=60, fg_color="#555", command=lambda: self.batch_add_folder(self.list_b))
        self.batch_b_btn.pack(side="left", padx=(0,5))
        self.clear_b_btn = ctk.CTkButton(self.btn_frame_b, text="清空", width=60, fg_color="darkred", hover_color="#8b0000", command=lambda: self.list_b.delete(0, tk.END))
        self.clear_b_btn.pack(side="left")

        # Options
        self.check_similar_var = ctk.BooleanVar(value=True)
        self.check_similar_switch = ctk.CTkSwitch(self.sidebar_frame, text="尋找相似圖片", variable=self.check_similar_var)
        self.check_similar_switch.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        # Size Filter
        self.size_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.size_frame.grid(row=8, column=0, padx=20, pady=10, sticky="ew")
        
        self.lbl_min_kb = ctk.CTkLabel(self.size_frame, text=languages.get_text("size_filter_min"))
        self.lbl_min_kb.pack(side="left")
        self.min_size_entry = ctk.CTkEntry(self.size_frame, width=60)
        self.min_size_entry.insert(0, "0")
        self.min_size_entry.pack(side="left", padx=5)

        self.lbl_max_kb = ctk.CTkLabel(self.size_frame, text=languages.get_text("size_filter_max"))
        self.lbl_max_kb.pack(side="left")
        self.max_size_entry = ctk.CTkEntry(self.size_frame, width=60, placeholder_text="∞")
        self.max_size_entry.pack(side="left", padx=5)

        # Start/Stop Buttons
        self.start_btn = ctk.CTkButton(self.sidebar_frame, text="開始掃描", fg_color="green", hover_color="darkgreen", command=self.start_scan)
        self.start_btn.grid(row=9, column=0, padx=20, pady=(20, 10))

        self.stop_btn = ctk.CTkButton(self.sidebar_frame, text="停止", fg_color="darkred", hover_color="red", state="disabled", command=self.stop_scan)
        self.stop_btn.grid(row=10, column=0, padx=20, pady=(0, 20))

        # Copy Unique Button
        self.copy_btn = ctk.CTkButton(self.sidebar_frame, text=languages.get_text("btn_copy_unique"), fg_color="gray", state="disabled", command=self.copy_unique)
        self.copy_btn.grid(row=11, column=0, padx=20, pady=(0, 20))

        # Language Select
        self.lang_label = ctk.CTkLabel(self.sidebar_frame, text=languages.get_text("lang_label"), anchor="w")
        self.lang_label.grid(row=12, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.lang_menu = ctk.CTkOptionMenu(self.sidebar_frame, values=["繁體中文", "English"], command=self.change_language)
        self.lang_menu.set("繁體中文" if languages.get_current_language() == "zh_TW" else "English")
        self.lang_menu.grid(row=13, column=0, padx=20, pady=(0, 20))

        # --- Main Content (Results) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=20, sticky="nsew")

        # Result List (Scrollable)
        self.result_scroll = ctk.CTkScrollableFrame(self.main_frame, label_text="比對結果")
        self.result_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Status Bar ---
        self.status_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.status_frame.grid(row=2, column=1, sticky="ew", padx=20, pady=(0, 20))
        
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.pack(side="left", padx=20, fill="x", expand=True, pady=10)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self.status_frame, text="準備就緒")
        self.status_label.pack(side="right", padx=20)

        # --- Helper Variables ---
        self.scanner = logic.ImageScanner(callback_progress=self.update_progress)
        self.scanning = False

        self.refresh_text() # Initial text set

    def change_language(self, choice):
        code = "zh_TW" if choice == "繁體中文" else "en_US"
        languages.set_language(code)
        self.refresh_text()

    def refresh_text(self):
        self.title(languages.get_text("app_title"))
        self.logo_label.configure(text=languages.get_text("sidebar_title"))
        self.folder_a_label.configure(text=languages.get_text("group_a_label"))
        self.add_a_btn.configure(text=languages.get_text("btn_add"))
        self.batch_a_btn.configure(text=languages.get_text("btn_batch"))
        self.clear_a_btn.configure(text=languages.get_text("btn_clear"))
        
        self.folder_b_label.configure(text=languages.get_text("group_b_label"))
        self.add_b_btn.configure(text=languages.get_text("btn_add"))
        self.batch_b_btn.configure(text=languages.get_text("btn_batch"))
        self.clear_b_btn.configure(text=languages.get_text("btn_clear"))
        
        self.check_similar_switch.configure(text=languages.get_text("check_similar"))
        self.lbl_min_kb.configure(text=languages.get_text("size_filter_min"))
        self.lbl_max_kb.configure(text=languages.get_text("size_filter_max")) # Need to save ref to labels
        
        if not self.scanning:
            self.start_btn.configure(text=languages.get_text("btn_start"))
            self.stop_btn.configure(text=languages.get_text("btn_stop"))
            self.status_label.configure(text=languages.get_text("status_ready") if self.progress_bar.get() == 0 else languages.get_text("status_complete"))
        else:
             self.start_btn.configure(text=languages.get_text("btn_scanning"))
             self.stop_btn.configure(text=languages.get_text("btn_stop"))
        
        if hasattr(self, 'unique_files') and self.unique_files:
             self.copy_btn.configure(text=languages.get_text("btn_copy_unique_count", len(self.unique_files)))
        else:
             self.copy_btn.configure(text=languages.get_text("btn_no_unique") if not hasattr(self, 'unique_files') else languages.get_text("btn_no_unique"))
             
        self.result_scroll.configure(label_text=languages.get_text("app_title")) # Scrollable frame label? No, label_text is for frame title usually... wait, ctk scrollable frame has label_text
        self.result_scroll.configure(label_text="Results") # Or dynamic
        
        self.lang_label.configure(text=languages.get_text("lang_label"))
        
        # We need to refresh results header if possible?
        # The result headers are labels inside a frame. 
        # Ideally we rebuild the header or keep references.
        # For simplicity, we might just clear results when language changes? Or just leave them until next scan? 
        # User might want to see existing results translated.
        # Let's try to update header labels if we kept references. We didn't.
        # So we might need to recreate the header.
        
        # Re-create header
        for widget in self.result_scroll.winfo_children():
             # Hacky way to find header frame?
             # Probably easier to just clear results or accept that old results stay in old language until rescan/refresh.
             # Or we can clear results for now to avoid confusion.
             pass


    def add_folder(self, listbox):
        folder = filedialog.askdirectory()
        if folder:
            items = listbox.get(0, tk.END)
            if folder not in items:
                listbox.insert(tk.END, folder)

    def batch_add_folder(self, listbox):
        root_folder = filedialog.askdirectory(title=languages.get_text("msg_select_root"))
        if not root_folder:
            return
            
        # Find immediate subdirectories
        subdirs = [os.path.join(root_folder, d) for d in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, d))]
        
        if not subdirs:
            messagebox.showinfo(languages.get_text("msg_title_info"), languages.get_text("msg_no_subdirs"))
            return

        # Callback to add selected
        def on_confirm(selected_paths):
            items = listbox.get(0, tk.END)
            count = 0
            for path in selected_paths:
                if path not in items:
                    listbox.insert(tk.END, path)
                    count += 1
            if count > 0:
                messagebox.showinfo(languages.get_text("msg_title_info"), languages.get_text("msg_added_folders", count))

        # Show dialog
        MultiSelectDialog(self, languages.get_text("msg_title_batch"), subdirs, on_confirm)

    def start_scan(self):
        if self.scanning:
            return

        folders_a = self.list_a.get(0, tk.END)
        folders_b = self.list_b.get(0, tk.END)

        if not folders_a:
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_no_folder_a"))
            return

        # Parse Size
        try:
            min_kb = float(self.min_size_entry.get()) if self.min_size_entry.get() else 0
            max_kb = float(self.max_size_entry.get()) if self.max_size_entry.get() else None
            
            min_bytes = int(min_kb * 1024)
            max_bytes = int(max_kb * 1024) if max_kb is not None else None
        except ValueError:
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_size_fmt"))
            return

        # Clear previous results
        for widget in self.result_scroll.winfo_children():
            widget.destroy()

        self.scanning = True
        self.start_btn.configure(state="disabled", text=languages.get_text("btn_scanning"))
        self.stop_btn.configure(state="normal", text=languages.get_text("btn_stop"))
        self.progress_bar.set(0)
        self.scanner.stop_requested = False

        # Run in thread
        threading.Thread(target=self.run_logic, args=(folders_a, folders_b, min_bytes, max_bytes), daemon=True).start()

    def stop_scan(self):
        if self.scanning:
            if messagebox.askyesno(languages.get_text("msg_title_stop"), languages.get_text("msg_confirm_stop")):
                self.scanner.stop_requested = True
                self.status_label.configure(text=languages.get_text("status_stopping"))
                self.stop_btn.configure(state="disabled", text=languages.get_text("btn_stopping"))

    def run_logic(self, folders_a, folders_b, min_bytes, max_bytes):
        try:
            results, unique_files = self.scanner.compare_folders(
                folders_a, 
                folders_b, 
                threshold=0.90, 
                check_similar=self.check_similar_var.get(),
                min_size=min_bytes,
                max_size=max_bytes
            )
            
            if self.scanner.stop_requested:
                self.after(0, lambda: messagebox.showinfo(languages.get_text("msg_title_stop"), languages.get_text("msg_scan_aborted")))
                self.after(0, self.reset_ui) # Reset without showing partial results? Or show?
                # User usually wants to see partial, but our parallel logic returns partial?
                # Logic returns [], [] if stopped. So clear results.
                self.unique_files = [] 
            else:
                self.unique_files = unique_files 
                self.after(0, self.show_results, results)
                
        except Exception as e:
            print(f"Error: {e}")
            self.after(0, lambda: messagebox.showerror(languages.get_text("msg_title_error"), str(e)))
        finally:
            self.scanning = False
            self.after(0, self.reset_ui)

    def update_progress(self, current, total, message):
        self.after(0, lambda: self.status_label.configure(text=message))
        if total > 0:
            progress = current / total
            self.after(0, lambda: self.progress_bar.set(progress))

    def reset_ui(self):
        self.start_btn.configure(state="normal", text=languages.get_text("btn_start"))
        self.stop_btn.configure(state="disabled", text=languages.get_text("btn_stop"))
        
        # Enable copy button if we have unique files
        if hasattr(self, 'unique_files') and self.unique_files:
            self.copy_btn.configure(state="normal", text=languages.get_text("btn_copy_unique_count", len(self.unique_files)))
        else:
            self.copy_btn.configure(state="disabled", text=languages.get_text("btn_no_unique"))

        if not self.scanner.stop_requested:
            self.status_label.configure(text=languages.get_text("status_complete"))
        else:
            self.status_label.configure(text=languages.get_text("status_stopped"))

    def show_results(self, results):
        if not results:
            lbl = ctk.CTkLabel(self.result_scroll, text=languages.get_text("res_no_match"), font=("Arial", 16))
            lbl.pack(pady=20)
            return

        # Header
        header = ctk.CTkFrame(self.result_scroll, fg_color="transparent")
        header.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(header, text=languages.get_text("res_header_type"), width=80, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header, text=languages.get_text("res_header_score"), width=60, anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(header, text=languages.get_text("res_header_files"), anchor="w", font=("Arial", 12, "bold")).pack(side="left", padx=5)

        for match in results:
            row = ctk.CTkFrame(self.result_scroll)
            row.pack(fill="x", pady=2)
            
            # Translate type
            type_text = languages.get_text("res_type_exact") if match['type'] == "完全相同" or match['type'] == "Exact Match" else languages.get_text("res_type_similar")
            # Note: logic.py originally returned "完全相同" or "視覺相似". Now we need to be careful.
            # logic.py still uses hardcoded types in _make_match? 
            # Ideally logic.py should return codes like "EXACT", "SIMILAR".
            # But let's check logic.py again. 
            
            color = "orange" if match['type'] in ["完全相同", "Exact Match", "EXACT"] else "lightblue"
            type_lbl = ctk.CTkLabel(row, text=type_text, text_color=color, width=80, anchor="w")
            type_lbl.pack(side="left", padx=5)

            score_lbl = ctk.CTkLabel(row, text=f"{match['score']}%", width=60, anchor="w")
            score_lbl.pack(side="left", padx=5)

            # File info
            name_a = os.path.basename(match['file_a'])
            name_b = os.path.basename(match['file_b'])
            info_lbl = ctk.CTkLabel(row, text=f"A: {name_a}\nB: {name_b}", anchor="w", justify="left")
            info_lbl.pack(side="left", padx=5, fill="x", expand=True)

            # View Button
            view_btn = ctk.CTkButton(row, text=languages.get_text("btn_view"), width=60, height=25, 
                                     command=lambda m=match: self.open_preview(m))
            view_btn.pack(side="right", padx=10, pady=5)

    def open_preview(self, match):
        PreviewWindow(self, match)

    def copy_unique(self):
        folders_b = self.list_b.get(0, tk.END)
        if not folders_b:
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_b_empty_copy"))
            return
        
        target_root = folders_b[0] # Use first folder
        
        if not os.path.isdir(target_root):
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_b_invalid"))
            return
            
        if not hasattr(self, 'unique_files') or not self.unique_files:
            messagebox.showinfo(languages.get_text("msg_title_info"), languages.get_text("msg_no_unique_copy"))
            return

        target_dir = os.path.join(target_root, "Compared_Pictures")
        try:
            os.makedirs(target_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_create_dir", e))
            return

        count = 0
        import shutil
        try:
            for filepath in self.unique_files:
                filename = os.path.basename(filepath)
                dest = os.path.join(target_dir, filename)
                
                # Handle duplicate names
                if os.path.exists(dest):
                    base, ext = os.path.splitext(filename)
                    dest = os.path.join(target_dir, f"{base}_copy{ext}")
                    
                shutil.copy2(filepath, dest)
                count += 1
            
            messagebox.showinfo(languages.get_text("msg_title_success"), languages.get_text("msg_copy_success", count, target_dir))
        except Exception as e:
            messagebox.showerror(languages.get_text("msg_title_error"), languages.get_text("msg_err_copy_fail", e))

class MultiSelectDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, options, callback):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x500")
        self.callback = callback
        self.check_vars = []
        
        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Controls
        ctrl_frame = ctk.CTkFrame(self, height=40)
        ctrl_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ctk.CTkButton(ctrl_frame, text=languages.get_text("btn_select_all"), width=80, command=self.select_all).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text=languages.get_text("btn_deselect_all"), width=80, command=self.deselect_all).pack(side="left", padx=5)
        ctk.CTkButton(ctrl_frame, text=languages.get_text("btn_confirm_add"), fg_color="green", width=100, command=self.confirm).pack(side="right", padx=5)

        # List
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Populate
        self.options = options # specific list of full paths
        for path in options:
            name = os.path.basename(path)
            var = ctk.BooleanVar(value=True) # Default selected
            chk = ctk.CTkCheckBox(self.scroll, text=name, variable=var)
            chk.pack(anchor="w", pady=2, padx=5)
            self.check_vars.append((path, var))

    def select_all(self):
        for _, var in self.check_vars:
            var.set(True)

    def deselect_all(self):
        for _, var in self.check_vars:
            var.set(False)

    def confirm(self):
        selected = [path for path, var in self.check_vars if var.get()]
        self.callback(selected)
        self.destroy()

class PreviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, match):
        super().__init__(parent)
        self.title(languages.get_text("msg_title_preview"))
        self.geometry("800x500")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Load images
        self.img_a = self.load_image(match['file_a'])
        self.img_b = self.load_image(match['file_b'])

        lbl_a = ctk.CTkLabel(self, text=languages.get_text("res_col_file_a") + f"\n{os.path.basename(match['file_a'])}", image=self.img_a, compound="bottom")
        lbl_a.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        lbl_b = ctk.CTkLabel(self, text=languages.get_text("res_col_file_b") + f"\n{os.path.basename(match['file_b'])}", image=self.img_b, compound="bottom")
        lbl_b.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Determine strict type
        strict_type = languages.get_text("res_type_exact") if match['type'] in ["完全相同", "Exact Match"] else languages.get_text("res_type_similar")
        info = ctk.CTkLabel(self, text=languages.get_text("res_info_match", strict_type, match['score']), font=("Arial", 16, "bold"))
        info.grid(row=1, column=0, columnspan=2, pady=10)

    def load_image(self, path):
        try:
            img = Image.open(path)
            # Resize logic
            img.thumbnail((380, 400))
            return ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
        except Exception as e:
            print(e)
            return None

import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = App()
    app.mainloop()
