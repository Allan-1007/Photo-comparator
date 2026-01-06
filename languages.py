import locale
import threading

# Copyright (c) 2025 Photo Comparator. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

# Language Dictionary
# Keys should be consistent across languages

TRANSLATIONS = {
    "zh_TW": {
        # Titles & Labels
        "app_title": "照片比對小幫手",
        "sidebar_title": "照片比對工具",
        "group_a_label": "群組 A (來源):",
        "group_b_label": "群組 B (若空則自我比對):",
        "options_label": "選項",
        "check_similar": "尋找相似圖片",
        "size_filter_min": "最小 KB:",
        "size_filter_max": "最大 KB:",
        
        # Buttons
        "btn_add": "新增",
        "btn_batch": "批次",
        "btn_clear": "清空",
        "btn_start": "開始掃描",
        "btn_scanning": "掃描中...",
        "btn_stop": "停止",
        "btn_stopping": "正在停止...",
        "btn_copy_unique": "複製獨有照片至 B",
        "btn_copy_unique_count": "複製 {} 張獨有照片至 B",
        "btn_no_unique": "無獨有照片可複製",
        "btn_view": "檢視",
        "btn_select_all": "全選",
        "btn_deselect_all": "全不選",
        "btn_confirm_add": "確定加入",
        
        # Status Messages
        "status_ready": "準備就緒",
        "status_stopping": "正在停止...",
        "status_stopped": "已停止",
        "status_complete": "掃描完成",
        "status_scanning_a": "正在掃描群組 A...",
        "status_scanning_b": "正在掃描群組 B...",
        "status_analyzing": "分析中 ({}/{})",
        "status_comparing": "比對中 ({}/{})",
        "status_finished": "完成！",

        # Results
        "res_header_type": "類型",
        "res_header_score": "相似度",
        "res_header_files": "檔案 A / 檔案 B",
        "res_type_exact": "完全相同",
        "res_type_similar": "視覺相似",
        "res_no_match": "未發現符合的圖片。",
        "res_col_file_a": "檔案 A",
        "res_col_file_b": "檔案 B",
        "res_info_match": "判定: {} ({}%)",

        # Dialogs / Messages
        "msg_title_info": "資訊",
        "msg_title_error": "錯誤",
        "msg_title_success": "成功",
        "msg_title_stop": "停止",
        "msg_title_batch": "批次選擇資料夾",
        "msg_title_preview": "圖片預覽",
        "msg_select_root": "選擇母資料夾 (將列出子資料夾)",
        "msg_no_subdirs": "該資料夾下沒有子資料夾！",
        "msg_added_folders": "已加入 {} 個資料夾。",
        "msg_err_no_folder_a": "請至少在群組 A 新增一個資料夾！",
        "msg_err_size_fmt": "檔案大小格式錯誤！請輸入數字。",
        "msg_confirm_stop": "確定要停止掃描嗎？",
        "msg_scan_aborted": "掃描已中止。",
        "msg_err_b_empty_copy": "群組 B 為空，無法決定複製目的地。",
        "msg_err_b_invalid": "群組 B 的第一個資料夾無效！",
        "msg_no_unique_copy": "沒有獨有照片可複製。",
        "msg_err_create_dir": "無法建立資料夾: {}",
        "msg_copy_success": "已複製 {} 張照片到\n{}",
        "msg_err_copy_fail": "複製失敗: {}",
        
        # UI
        "lang_label": "語言 (Language):"
    },
    "en_US": {
        # Titles & Labels
        "app_title": "Photo Comparator Helper",
        "sidebar_title": "Photo Comparator",
        "group_a_label": "Group A (Source):",
        "group_b_label": "Group B (Target, optional):",
        "options_label": "Options",
        "check_similar": "Find Similar Images",
        "size_filter_min": "Min KB:",
        "size_filter_max": "Max KB:",
        
        # Buttons
        "btn_add": "Add",
        "btn_batch": "Batch",
        "btn_clear": "Clear",
        "btn_start": "Start Scan",
        "btn_scanning": "Scanning...",
        "btn_stop": "Stop",
        "btn_stopping": "Stopping...",
        "btn_copy_unique": "Copy Unique to B",
        "btn_copy_unique_count": "Copy {} Unique to B",
        "btn_no_unique": "No Unique to Copy",
        "btn_view": "View",
        "btn_select_all": "Select All",
        "btn_deselect_all": "Deselect All",
        "btn_confirm_add": "Confirm Add",
        
        # Status Messages
        "status_ready": "Ready",
        "status_stopping": "Stopping...",
        "status_stopped": "Stopped",
        "status_complete": "Scan Complete",
        "status_scanning_a": "Scanning Group A...",
        "status_scanning_b": "Scanning Group B...",
        "status_analyzing": "Analyzing ({}/{})",
        "status_comparing": "Comparing ({}/{})",
        "status_finished": "Finished!",

        # Results
        "res_header_type": "Type",
        "res_header_score": "Score",
        "res_header_files": "File A / File B",
        "res_type_exact": "Exact Match",
        "res_type_similar": "Visual Similar",
        "res_no_match": "No matching images found.",
        "res_col_file_a": "File A",
        "res_col_file_b": "File B",
        "res_info_match": "Verdict: {} ({}%)",

        # Dialogs / Messages
        "msg_title_info": "Info",
        "msg_title_error": "Error",
        "msg_title_success": "Success",
        "msg_title_stop": "Stop",
        "msg_title_batch": "Batch Select Folders",
        "msg_title_preview": "Image Preview",
        "msg_select_root": "Select Root Folder",
        "msg_no_subdirs": "No subdirectories found!",
        "msg_added_folders": "Added {} folders.",
        "msg_err_no_folder_a": "Please add at least one folder to Group A!",
        "msg_err_size_fmt": "Invalid size format! Please enter numbers.",
        "msg_confirm_stop": "Are you sure you want to stop scanning?",
        "msg_scan_aborted": "Scan aborted.",
        "msg_err_b_empty_copy": "Group B is empty, cannot determine destination.",
        "msg_err_b_invalid": "The first folder of Group B is invalid!",
        "msg_no_unique_copy": "No unique photos to copy.",
        "msg_err_create_dir": "Cannot create directory: {}",
        "msg_copy_success": "Copied {} photos to\n{}",
        "msg_err_copy_fail": "Copy failed: {}",
        
        # UI
        "lang_label": "Language:"
    }
}

current_lang = "zh_TW"

def set_language(lang_code):
    global current_lang
    if lang_code in TRANSLATIONS:
        current_lang = lang_code

def get_current_language():
    return current_lang

def get_text(key, *args):
    """
    Get translated text for key. 
    If args are provided, format the string.
    """
    lang_dict = TRANSLATIONS.get(current_lang, TRANSLATIONS["zh_TW"])
    text = lang_dict.get(key, key)
    
    if args:
        try:
            return text.format(*args)
        except:
            return text
    return text
