# -*- coding: utf-8 -*-
import webview
import threading
import json
import os
import sys
import multiprocessing
from audio_processor import AudioProcessor
from translator import translate_srt_file
import utils
from gui import HTML



class Bridge:
    def __init__(self):
        self.window = None
        self.audio_processor = AudioProcessor()
        self.settings_file = "settings.json"
        self.settings = self.load_settings()
        self.translation_cancel_event = threading.Event()   # <-- جديد


    def select_file(self, file_types):
        result = self.window.create_file_dialog(webview.FileDialog.OPEN, file_types=file_types)
        return result[0] if result else None

    def select_files(self, file_types):
        result = self.window.create_file_dialog(webview.FileDialog.OPEN, allow_multiple=True, file_types=file_types)
        return result if result else None

    def select_folder(self):
        result = self.window.create_file_dialog(webview.FileDialog.FOLDER)
        return result[0] if result else None

    def save_file_dialog(self, title="Save File", default_ext=".srt"):
        result = self.window.create_file_dialog(webview.FileDialog.SAVE, file_types=[f"Files (*{default_ext})"])
        return result[0] if result else None

    def safe_execute_js(self, js_code):
        if self.window:
            try:
                self.window.evaluate_js(js_code)
            except Exception:
                pass

    def update_progress(self, percent, status):
        safe_status = json.dumps(status)
        js_code = f"updateProgress({percent}, {safe_status})"
        self.safe_execute_js(js_code)

    def show_toast(self, message, type='info'):
        safe_message = json.dumps(message)
        js_code = f"showToast({safe_message}, '{type}')"
        self.safe_execute_js(js_code)
    # ---------------------------------

    def convert_video(self, video_path, model, lang, save_path=None):
        def _run():
            try:
                srt_content = self.audio_processor.convert_video_to_srt(
                    video_path, model, lang, self.update_progress
                )
                if srt_content:
                    output_path = save_path if save_path else os.path.splitext(video_path)[0] + ".srt"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(srt_content)
                    self.show_toast(f"تم حفظ الملف في: {output_path}", "success")
            except Exception as e:
                self.show_toast(f"خطأ: {str(e)}", "error")
        
        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

    def translate_srt(self, input_path, target_lang, save_path=None, source_lang='auto', options=None):
        self.translation_cancel_event = threading.Event()
    
        if not save_path:
            save_path = os.path.splitext(input_path)[0] + f"_{target_lang}.srt"
    
        keep_format = options.get('keepFormat', True) if options else True
        trans_numbers = options.get('transNumbers', False) if options else False
        keep_indexes = options.get('keepIndexes', True) if options else True

        success = translate_srt_file(
            input_path, save_path, target_lang, 
            self.update_progress, 
            self.translation_cancel_event,       
            source_lang=source_lang,
            keep_format=keep_format,
            trans_numbers=trans_numbers,
            keep_indexes=keep_indexes
        )
        if success:
            self.show_toast(f"تم حفظ الترجمة في: {save_path}", "success")
        return success


    def merge_srt(self, file_paths):
        save_path = self.save_file_dialog("Save Merged SRT", ".srt")
        if save_path:
            utils.merge_srt_files(file_paths, save_path)
            self.show_toast("تم دمج الملفات بنجاح", "success")

    def split_srt(self, file_path, seconds):
        prefix = os.path.splitext(file_path)[0]
        utils.split_srt_by_seconds(file_path, int(seconds), prefix)
        self.show_toast("تم تقسيم الملف بنجاح", "success")

    def adjust_time(self, file_path, delta):
        output_path = os.path.splitext(file_path)[0] + "_adjusted.srt"
        utils.adjust_srt_timing(file_path, output_path, delta)
        self.show_toast("تم تعديل التوقيت بنجاح", "success")

    def change_encoding(self, file_path):
        output_path = os.path.splitext(file_path)[0] + "_utf8.srt"
        utils.change_srt_encoding(file_path, output_path)
        self.show_toast("تم تغيير الترميز إلى UTF-8", "success")

    def extract_text(self, file_path):
        output_path = os.path.splitext(file_path)[0] + "_raw.txt"
        utils.extract_raw_text(file_path, output_path)
        self.show_toast("تم استخراج النص الخام بنجاح", "success")

    def export_word(self, file_path):
        output_path = os.path.splitext(file_path)[0] + ".docx"
        utils.export_to_word(file_path, output_path)
        self.show_toast("تم تصدير ملف Word بنجاح", "success")

    def batch_process_files(self, file_paths, action_type, options=None):
        def worker():
            total = len(file_paths)
            if total == 0: return self.show_toast("لم يتم اختيار أي ملفات", "error")
            
            for i, f in enumerate(file_paths):
                if self.audio_processor.cancel_event.is_set(): break
                self.update_progress(int((i/total)*100), f"جاري المعالجة ({i+1}/{total}): {os.path.basename(f)}")
                
                if action_type == 'convert':
                    try:
                        srt_content = self.audio_processor.convert_video_to_srt(
                            f, self.settings.get('model', 'small'), self.settings.get('lang', 'ar'), self.update_progress
                        )
                        if srt_content:
                            output_path = os.path.splitext(f)[0] + ".srt"
                            with open(output_path, 'w', encoding='utf-8') as out_f:
                                out_f.write(srt_content)
                    except Exception as e:
                        self.show_toast(f"خطأ في {os.path.basename(f)}: {str(e)}", "error")
                else:
                    self.translate_srt(f, self.settings.get('lang', 'ar'), options=options)
            
            self.show_toast("اكتملت المعالجة الدفعية للملفات بنجاح", "success")
            self.update_progress(100, "تم الانتهاء")
        
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    def batch_process_folder(self, folder_path, action_type, options=None):
        if action_type == 'convert':
            exts = ('.mp4', '.mkv', '.avi', '.mov')
        else:
            exts = ('.srt',)
            
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(exts)]
        if not files: return self.show_toast(f"لا توجد ملفات متوافقة في المجلد المختار", "error")
        self.batch_process_files(files, action_type, options=options)

    def merge_folder(self, folder_path):
        files = sorted([os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith('.srt')])
        if not files: return self.show_toast("لا توجد ملفات SRT لدمجها", "error")
        self.merge_srt(files)
# جديدو
    def cancel_operation(self):
    # إلغاء عملية تحويل الفيديو (إذا كانت نشطة)
        self.audio_processor.cancel()
    # إلغاء عملية الترجمة (إذا كانت نشطة)
        self.translation_cancel_event.set()

    def save_srt_content(self, content):
        save_path = self.save_file_dialog("Save Edited SRT", ".srt")
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"model": "small", "lang": "ar"}

    def save_settings(self, settings):
        self.settings.update(settings)
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    bridge = Bridge()
    window = webview.create_window(
        'TarjemVid-AI',
        html=HTML,
        js_api=bridge,
        width=1200,
        height=800,
        background_color='#0f172a'
    )
    bridge.window = window
    
    # خيار إضافي  لويندوز 10/11 لمنع تعليق خيوط WebView2
    webview.start(debug=False) 
    # ظهور DEvTools قد يسبب مشاكل في بعض الأحيان، لذا تم تعطيله في هذا السطر.
