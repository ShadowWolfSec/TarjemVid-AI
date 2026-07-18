# -*- coding: utf-8 -*-
"""
Created on Fri Dec 12 17:13:02 2025

@author: rasheed
"""

# import sys
# import requests
# import json
# import os
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox, scrolledtext
# import threading
# from pathlib import Path
# import urllib.parse
# import urllib.request
# from datetime import datetime
# import subprocess
# import whisper
# import time
# from datetime import timedelta

# ========== المكتبات الأساسية - يجب أن تكون في البداية ==========
# import sys
# import whisper  # 1. استيراد Whisper أولاً
# import torch    # 2. يضمن تحميل مكتبات PyTorch الأساسية
# import os
# import json
# import time
# # ... باقي المكتبات الأساسية

# # ========== مكتبات واجهة المستخدم - بعد ذلك ==========
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox, scrolledtext
# # ... باقي مكتبات الواجهة والبرنامج

# ======== هذان السطران يجب أن يكونا أول شيء في الملف ========
import sys
import torch
# ========================================================

# ثم باقي المكتبات بنفس الترتيب القديم
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import urllib.parse
import urllib.request
import subprocess

# بعدها المكتبات الأخرى
import whisper  # الآن torch محمل مسبقاً
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading

class SRTTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.setup_app()
        self.setup_variables()
        self.setup_ui()
        self.setup_menu()
        
    def setup_app(self):
        self.root.title("🌍 مترجم SRT المتقدم - تحويل + ترجمة")
        self.root.geometry("1100x850")
        self.root.configure(bg="#1a1a2e")
        
    def setup_variables(self):
        # متغيرات التحويل
        self.video_path = tk.StringVar()
        self.output_srt_path = tk.StringVar()
        self.model_size = tk.StringVar(value="tiny")
        
        # متغيرات الترجمة
        self.input_srt_path = tk.StringVar()
        self.translated_srt_path = tk.StringVar()
        self.target_language = tk.StringVar(value="ar")
        self.source_language = tk.StringVar(value="auto")
        
        # حالة التطبيق
        self.status = tk.StringVar(value="جاهز للاستخدام")
        self.progress = tk.IntVar(value=0)
        self.is_converting = False
        self.is_translating = False
        
        # اللغات المدعومة
        self.languages = {
            "العربية": "ar",
            "الإنجليزية": "en",
            "الفرنسية": "fr",
            "الألمانية": "de",
            "الإسبانية": "es",
            "الإيطالية": "it",
            "البرتغالية": "pt",
            "الروسية": "ru",
            "الصينية": "zh-CN",
            "اليابانية": "ja",
            "الكورية": "ko",
            "التركية": "tr",
            "الفارسية": "fa",
            "العبرية": "he",
            "الهندية": "hi"
        }
        
        # نماذج Whisper
        self.models = {
            "tiny (أسرع)": "tiny",
            "base (متوازن)": "base",
            "small (جيد)": "small",
            "medium (متقدم)": "medium",
            "large (الأفضل)": "large"
        }
        
    def setup_ui(self):
        # Notebook لتبويب الواجهة
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # تبويب التحويل (Video to SRT)
        self.convert_tab = tk.Frame(self.notebook, bg="#162447")
        self.notebook.add(self.convert_tab, text="🎬 تحويل الفيديو إلى SRT")
        
        # تبويب الترجمة (SRT Translation)
        self.translate_tab = tk.Frame(self.notebook, bg="#1f4068")
        self.notebook.add(self.translate_tab, text="🌍 ترجمة ملف SRT")
        
        # تبويب الأدوات المتقدمة
        self.tools_tab = tk.Frame(self.notebook, bg="#1b1b2f")
        self.notebook.add(self.tools_tab, text="⚙️ أدوات متقدمة")
        
        self.setup_convert_tab()
        self.setup_translate_tab()
        self.setup_tools_tab()
        self.setup_status_bar()
        
    def setup_convert_tab(self):
        # عنوان القسم
        title_label = tk.Label(
            self.convert_tab,
            text="🎬 تحويل الفيديو إلى ملف SRT",
            font=("Arial", 18, "bold"),
            bg="#162447",
            fg="#e43f5a"
        )
        title_label.pack(pady=(20, 10))
        
        # إطار اختيار الفيديو
        video_frame = tk.LabelFrame(
            self.convert_tab,
            text="📹 اختيار ملف الفيديو",
            font=("Arial", 12, "bold"),
            bg="#162447",
            fg="white",
            relief=tk.GROOVE
        )
        video_frame.pack(fill="x", padx=20, pady=10)
        
        # صف اختيار الفيديو
        video_row = tk.Frame(video_frame, bg="#162447")
        video_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            video_row,
            text="مسار الفيديو:",
            font=("Arial", 11),
            bg="#162447",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.video_entry = tk.Entry(
            video_row,
            textvariable=self.video_path,
            width=50,
            font=("Arial", 11),
            bg="#1f4068",
            fg="white",
            insertbackground="white"
        )
        self.video_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Button(
            video_row,
            text="تصفح...",
            command=self.browse_video,
            bg="#e43f5a",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left")
        
        # إطار إعدادات التحويل
        settings_frame = tk.LabelFrame(
            self.convert_tab,
            text="⚙️ إعدادات التحويل",
            font=("Arial", 12, "bold"),
            bg="#162447",
            fg="white",
            relief=tk.GROOVE
        )
        settings_frame.pack(fill="x", padx=20, pady=10)
        
        # صف النموذج
        model_row = tk.Frame(settings_frame, bg="#162447")
        model_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            model_row,
            text="نموذج Whisper:",
            font=("Arial", 11),
            bg="#162447",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.model_combo = ttk.Combobox(
            model_row,
            textvariable=self.model_size,
            values=list(self.models.keys()),
            state="readonly",
            width=25,
            font=("Arial", 11)
        )
        self.model_combo.pack(side="left", padx=(0, 30))
        
        # صف اللغة
        lang_row = tk.Frame(settings_frame, bg="#162447")
        lang_row.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            lang_row,
            text="لغة الفيديو:",
            font=("Arial", 11),
            bg="#162447",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.convert_lang_combo = ttk.Combobox(
            lang_row,
            values=list(self.languages.keys()),
            state="readonly",
            width=20,
            font=("Arial", 11)
        )
        self.convert_lang_combo.set("الإنجليزية")
        self.convert_lang_combo.pack(side="left")
        
        # إطار اسم الملف الناتج
        output_frame = tk.LabelFrame(
            self.convert_tab,
            text="💾 حفظ الملف الناتج",
            font=("Arial", 12, "bold"),
            bg="#162447",
            fg="white",
            relief=tk.GROOVE
        )
        output_frame.pack(fill="x", padx=20, pady=10)
        
        output_row = tk.Frame(output_frame, bg="#162447")
        output_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            output_row,
            text="اسم ملف SRT:",
            font=("Arial", 11),
            bg="#162447",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.output_srt_entry = tk.Entry(
            output_row,
            textvariable=self.output_srt_path,
            width=40,
            font=("Arial", 11),
            bg="#1f4068",
            fg="white",
            insertbackground="white"
        )
        self.output_srt_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Button(
            output_row,
            text="📁",
            command=self.browse_output_folder,
            bg="#1f4068",
            fg="white",
            font=("Arial", 12),
            width=3,
            cursor="hand2"
        ).pack(side="left")
        
        # زر التحويل
        convert_btn = tk.Button(
            self.convert_tab,
            text="🚀 بدء تحويل الفيديو إلى SRT",
            command=self.start_video_conversion,
            bg="#e43f5a",
            fg="white",
            font=("Arial", 14, "bold"),
            width=30,
            height=2,
            cursor="hand2"
        )
        convert_btn.pack(pady=20)
        
        # معلومات إضافية
        info_label = tk.Label(
            self.convert_tab,
            text="💡 الميزات:\n• تحويل أي فيديو إلى نص\n• دعم 99 لغة تلقائياً\n• حفظ التوقيتات الدقيقة\n• دعم النماذج المختلفة",
            font=("Arial", 10),
            bg="#162447",
            fg="#a9a9a9",
            justify="left"
        )
        info_label.pack(pady=10)
        
    def setup_translate_tab(self):
        # عنوان القسم
        title_label = tk.Label(
            self.translate_tab,
            text="🌍 ترجمة ملفات SRT",
            font=("Arial", 18, "bold"),
            bg="#1f4068",
            fg="#21e6c1"
        )
        title_label.pack(pady=(20, 10))
        
        # إطار ملف الإدخال
        input_frame = tk.LabelFrame(
            self.translate_tab,
            text="📄 ملف SRT المدخل",
            font=("Arial", 12, "bold"),
            bg="#1f4068",
            fg="white",
            relief=tk.GROOVE
        )
        input_frame.pack(fill="x", padx=20, pady=10)
        
        input_row = tk.Frame(input_frame, bg="#1f4068")
        input_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            input_row,
            text="ملف SRT:",
            font=("Arial", 11),
            bg="#1f4068",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.input_srt_entry = tk.Entry(
            input_row,
            textvariable=self.input_srt_path,
            width=50,
            font=("Arial", 11),
            bg="#162447",
            fg="white",
            insertbackground="white"
        )
        self.input_srt_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Button(
            input_row,
            text="تصفح...",
            command=self.browse_srt_file,
            bg="#21e6c1",
            fg="#1f4068",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        ).pack(side="left")
        
        # إطار إعدادات الترجمة
        trans_settings_frame = tk.LabelFrame(
            self.translate_tab,
            text="⚙️ إعدادات الترجمة",
            font=("Arial", 12, "bold"),
            bg="#1f4068",
            fg="white",
            relief=tk.GROOVE
        )
        trans_settings_frame.pack(fill="x", padx=20, pady=10)
        
        # صف اللغة المصدر
        src_row = tk.Frame(trans_settings_frame, bg="#1f4068")
        src_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            src_row,
            text="لغة المصدر:",
            font=("Arial", 11),
            bg="#1f4068",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.source_lang_combo = ttk.Combobox(
            src_row,
            textvariable=self.source_language,
            values=["تلقائي"] + list(self.languages.keys()),
            state="readonly",
            width=20,
            font=("Arial", 11)
        )
        self.source_lang_combo.set("تلقائي")
        self.source_lang_combo.pack(side="left", padx=(0, 30))
        
        # صف اللغة الهدف
        tgt_row = tk.Frame(trans_settings_frame, bg="#1f4068")
        tgt_row.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(
            tgt_row,
            text="لغة الهدف:",
            font=("Arial", 11),
            bg="#1f4068",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.target_lang_combo = ttk.Combobox(
            tgt_row,
            textvariable=self.target_language,
            values=list(self.languages.keys()),
            state="readonly",
            width=20,
            font=("Arial", 11)
        )
        self.target_lang_combo.set("العربية")
        self.target_lang_combo.pack(side="left")
        
        # إطار حفظ الملف المترجم
        trans_output_frame = tk.LabelFrame(
            self.translate_tab,
            text="💾 حفظ الملف المترجم",
            font=("Arial", 12, "bold"),
            bg="#1f4068",
            fg="white",
            relief=tk.GROOVE
        )
        trans_output_frame.pack(fill="x", padx=20, pady=10)
        
        trans_output_row = tk.Frame(trans_output_frame, bg="#1f4068")
        trans_output_row.pack(fill="x", padx=10, pady=10)
        
        tk.Label(
            trans_output_row,
            text="الملف المترجم:",
            font=("Arial", 11),
            bg="#1f4068",
            fg="white"
        ).pack(side="left", padx=(0, 10))
        
        self.translated_srt_entry = tk.Entry(
            trans_output_row,
            textvariable=self.translated_srt_path,
            width=40,
            font=("Arial", 11),
            bg="#162447",
            fg="white",
            insertbackground="white"
        )
        self.translated_srt_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        tk.Button(
            trans_output_row,
            text="📁",
            command=self.browse_translation_output,
            bg="#162447",
            fg="white",
            font=("Arial", 12),
            width=3,
            cursor="hand2"
        ).pack(side="left")
        
        # زر الترجمة
        translate_btn = tk.Button(
            self.translate_tab,
            text="🌐 بدء ترجمة ملف SRT",
            command=self.start_srt_translation,
            bg="#21e6c1",
            fg="#1f4068",
            font=("Arial", 14, "bold"),
            width=30,
            height=2,
            cursor="hand2"
        )
        translate_btn.pack(pady=20)
        
        # خيارات متقدمة للترجمة
        options_frame = tk.Frame(self.translate_tab, bg="#1f4068")
        options_frame.pack(pady=10)
        
        self.preserve_formatting = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options_frame,
            text="الحفاظ على التنسيق",
            variable=self.preserve_formatting,
            bg="#1f4068",
            fg="white",
            selectcolor="#1f4068",
            font=("Arial", 10)
        ).pack(side="left", padx=10)
        
        self.translate_numbers = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options_frame,
            text="ترجمة الأرقام",
            variable=self.translate_numbers,
            bg="#1f4068",
            fg="white",
            selectcolor="#1f4068",
            font=("Arial", 10)
        ).pack(side="left", padx=10)
        
    def setup_tools_tab(self):
        title_label = tk.Label(
            self.tools_tab,
            text="⚙️ أدوات متقدمة لملفات SRT",
            font=("Arial", 18, "bold"),
            bg="#1b1b2f",
            fg="#ffbd39"
        )
        title_label.pack(pady=(20, 10))
        
        # أدوات التحويل
        tools_frame = tk.Frame(self.tools_tab, bg="#1b1b2f")
        tools_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # أداة 1: دمج ملفات SRT
        merge_btn = tk.Button(
            tools_frame,
            text="🔄 دمج ملفات SRT",
            command=self.merge_srt_files,
            bg="#162447",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        merge_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # أداة 2: تقسيم ملف SRT
        split_btn = tk.Button(
            tools_frame,
            text="✂️ تقسيم ملف SRT",
            command=self.split_srt_file,
            bg="#1f4068",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        split_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # أداة 3: تعديل التوقيتات
        adjust_btn = tk.Button(
            tools_frame,
            text="⏱️ تعديل التوقيتات",
            command=self.adjust_timings,
            bg="#162447",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        adjust_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # أداة 4: تحويل الترميز
        encoding_btn = tk.Button(
            tools_frame,
            text="🔤 تغيير الترميز",
            command=self.change_encoding,
            bg="#1f4068",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        encoding_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # أداة 5: استخراج النص فقط
        extract_btn = tk.Button(
            tools_frame,
            text="📝 استخراج النص فقط",
            command=self.extract_text_only,
            bg="#162447",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        extract_btn.grid(row=2, column=0, padx=10, pady=10)
        
        # أداة 6: تصدير إلى Word
        export_btn = tk.Button(
            tools_frame,
            text="📄 تصدير إلى Word",
            command=self.export_to_word,
            bg="#1f4068",
            fg="white",
            font=("Arial", 12, "bold"),
            width=25,
            height=2,
            cursor="hand2"
        )
        export_btn.grid(row=2, column=1, padx=10, pady=10)
        
        # منطقة المعاينة
        preview_frame = tk.LabelFrame(
            self.tools_tab,
            text="👁️ معاينة الملف",
            font=("Arial", 12, "bold"),
            bg="#1b1b2f",
            fg="white",
            relief=tk.GROOVE
        )
        preview_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=10,
            font=("Courier New", 10),
            bg="#0f3460",
            fg="white",
            wrap=tk.WORD
        )
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=10)
        
    def setup_status_bar(self):
        # شريط الحالة
        status_frame = tk.Frame(self.root, bg="#0f3460", height=30)
        status_frame.pack(fill="x", side="bottom")
        status_frame.pack_propagate(False)
        
        # شريط التقدم
        self.progress_bar = ttk.Progressbar(
            status_frame,
            variable=self.progress,
            maximum=100,
            length=300
        )
        self.progress_bar.pack(side="left", padx=(10, 20))
        
        # نص الحالة
        tk.Label(
            status_frame,
            textvariable=self.status,
            font=("Arial", 10),
            bg="#0f3460",
            fg="#21e6c1"
        ).pack(side="left", padx=(0, 10))
        
        # معلومات النظام
        sys_info = f"Python {sys.version.split()[0]} | SRT Translator Pro"
        tk.Label(
            status_frame,
            text=sys_info,
            font=("Arial", 9),
            bg="#0f3460",
            fg="#a9a9a9"
        ).pack(side="right", padx=10)
        
    def setup_menu(self):
        menubar = tk.Menu(self.root, bg="#162447", fg="white")
        self.root.config(menu=menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1f4068", fg="white")
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="فتح فيديو...", command=self.browse_video)
        file_menu.add_command(label="فتح ملف SRT...", command=self.browse_srt_file)
        file_menu.add_separator()
        file_menu.add_command(label="الحفظ السريع", command=self.quick_save)
        file_menu.add_command(label="حفظ باسم...", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.root.quit)
        
        # قائمة التحرير
        edit_menu = tk.Menu(menubar, tearoff=0, bg="#1f4068", fg="white")
        menubar.add_cascade(label="تحرير", menu=edit_menu)
        edit_menu.add_command(label="نسخ", command=self.copy_text)
        edit_menu.add_command(label="لصق", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="تعديل SRT", command=self.edit_srt)
        
        # قائمة الأدوات
        tools_menu = tk.Menu(menubar, tearoff=0, bg="#1f4068", fg="white")
        menubar.add_cascade(label="أدوات", menu=tools_menu)
        tools_menu.add_command(label="تحويل دفعة", command=self.batch_convert)
        tools_menu.add_command(label="ترجمة دفعة", command=self.batch_translate)
        tools_menu.add_separator()
        tools_menu.add_command(label="الإعدادات", command=self.open_settings)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0, bg="#1f4068", fg="white")
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="تعليمات", command=self.show_help)
        help_menu.add_command(label="عن البرنامج", command=self.show_about)
        
    # ========== الوظائف الأساسية ==========
    
    def browse_video(self):
        filetypes = [
            ("ملفات الفيديو", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
            ("كل الملفات", "*.*")
        ]
        
        filename = filedialog.askopenfilename(title="اختر ملف فيديو", filetypes=filetypes)
        if filename:
            self.video_path.set(filename)
            
            # اقتراح اسم ملف الإخراج
            video_name = Path(filename).stem
            self.output_srt_path.set(f"{video_name}.srt")
            
            self.log_message(f"📹 تم تحميل الفيديو: {Path(filename).name}")
    
    def browse_srt_file(self):
        filetypes = [("ملفات SRT", "*.srt"), ("كل الملفات", "*.*")]
        filename = filedialog.askopenfilename(title="اختر ملف SRT", filetypes=filetypes)
        if filename:
            self.input_srt_path.set(filename)
            
            # اقتراح اسم للملف المترجم
            srt_name = Path(filename).stem
            lang_code = self.languages.get(self.target_language.get(), "ar")
            self.translated_srt_path.set(f"{srt_name}_{lang_code}.srt")
            
            self.log_message(f"📄 تم تحميل ملف SRT: {Path(filename).name}")
            
            # معاينة الملف
            self.preview_srt_file(filename)
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="اختر مجلد الإخراج")
        if folder:
            current_file = self.output_srt_path.get()
            if current_file:
                new_path = Path(folder) / Path(current_file).name
                self.output_srt_path.set(str(new_path))
    
    def browse_translation_output(self):
        filetypes = [("ملفات SRT", "*.srt")]
        filename = filedialog.asksaveasfilename(
            title="حفظ الملف المترجم",
            defaultextension=".srt",
            filetypes=filetypes
        )
        if filename:
            self.translated_srt_path.set(filename)
    
    def start_video_conversion(self):
        if not self.video_path.get():
            messagebox.showerror("خطأ", "الرجاء اختيار ملف فيديو أولاً")
            return
        
        if self.is_converting:
            messagebox.showwarning("تنبيه", "عملية تحويل قيد التنفيذ بالفعل")
            return
        
        # تشغيل التحويل في خيط منفصل
        thread = threading.Thread(target=self.convert_video_to_srt)
        thread.daemon = True
        thread.start()
    
    def start_srt_translation(self):
        if not self.input_srt_path.get():
            messagebox.showerror("خطأ", "الرجاء اختيار ملف SRT للترجمة")
            return
        
        if self.is_translating:
            messagebox.showwarning("تنبيه", "عملية ترجمة قيد التنفيذ بالفعل")
            return
        
        # تشغيل الترجمة في خيط منفصل
        thread = threading.Thread(target=self.translate_srt_file)
        thread.daemon = True
        thread.start()
    
    def convert_video_to_srt(self):
        """تحويل الفيديو إلى SRT باستخدام Whisper"""
        self.is_converting = True
        self.status.set("جاري تحميل النموذج...")
        self.progress.set(10)
        
        try:
            video_path = self.video_path.get()
            output_srt_path = self.output_srt_path.get()
            
            if not output_srt_path:
                output_srt_path = f"{Path(video_path).stem}.srt"
                self.output_srt_path.set(output_srt_path)
            
            model_key = self.model_combo.get()
            model_name = self.models.get(model_key, "tiny")
            
            self.log_message(f"\n{'='*60}")
            self.log_message(f"🎬 بدء تحويل الفيديو: {Path(video_path).name}")
            self.log_message(f"📄 الملف الناتج: {output_srt_path}")
            self.log_message(f"🧠 النموذج: {model_key}")
            self.log_message(f"{'='*60}")
            
            # استخراج الصوت
            self.status.set("جاري استخراج الصوت...")
            self.progress.set(20)
            
            audio_path = f"temp_audio_{int(time.time())}.wav"
            cmd = ['ffmpeg', '-i', video_path, '-acodec', 'pcm_s16le', '-ac', '1', 
                   '-ar', '16000', '-y', audio_path]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_message("❌ فشل استخراج الصوت", "error")
                return
            
            self.log_message("✅ تم استخراج الصوت")
            self.progress.set(30)
            
            # تحميل النموذج
            self.status.set("جاري تحميل نموذج Whisper...")
            self.progress.set(40)
            
            try:
                model = whisper.load_model(model_name)
                self.log_message(f"✅ تم تحميل النموذج: {model_name}")
            except Exception as e:
                self.log_message(f"❌ خطأ في تحميل النموذج: {str(e)}", "error")
                return
            
            # التحويل
            self.status.set("جاري تحويل الصوت إلى نص...")
            self.progress.set(50)
            
            try:
                result = model.transcribe(
                    audio_path,
                    language="en",
                    word_timestamps=False,
                    fp16=False
                )
                self.log_message("✅ اكتمل التحويل النصي")
                self.progress.set(70)
            except Exception as e:
                self.log_message(f"❌ خطأ في التحويل: {str(e)}", "error")
                return
            
            # حفظ كـ SRT
            self.status.set("جاري حفظ ملف SRT...")
            self.progress.set(80)
            
            with open(output_srt_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(result['segments']):
                    start_time = self.format_time_srt(segment['start'])
                    end_time = self.format_time_srt(segment['end'])
                    
                    f.write(f"{i+1}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{segment['text'].strip()}\n\n")
            
            self.progress.set(90)
            
            # تنظيف
            if os.path.exists(audio_path):
                os.remove(audio_path)
            
            # إحصائيات
            word_count = len(result['text'].split())
            segment_count = len(result['segments'])
            
            self.log_message(f"\n📊 إحصائيات التحويل:")
            self.log_message(f"   ✅ المقاطع: {segment_count}")
            self.log_message(f"   ✅ الكلمات: {word_count}")
            self.log_message(f"   💾 الملف: {Path(output_srt_path).name}")
            
            self.progress.set(100)
            self.status.set("اكتمل التحويل بنجاح!")
            
            messagebox.showinfo(
                "نجاح",
                f"تم تحويل الفيديو بنجاح!\n\n"
                f"الملف: {Path(output_srt_path).name}\n"
                f"المقاطع: {segment_count}\n"
                f"الكلمات: {word_count}"
            )
            
            # تعبئة حقل الإدخال للترجمة تلقائياً
            self.input_srt_path.set(output_srt_path)
            
        except Exception as e:
            self.log_message(f"❌ خطأ غير متوقع: {str(e)}", "error")
            messagebox.showerror("خطأ", f"حدث خطأ أثناء التحويل:\n{str(e)}")
            self.status.set("فشل التحويل")
        finally:
            self.is_converting = False
    
    def translate_srt_file(self):
        """ترجمة ملف SRT باستخدام Google Translate"""
        self.is_translating = True
        self.status.set("جاري تحميل ملف SRT...")
        self.progress.set(10)
        
        try:
            input_srt = self.input_srt_path.get()
            output_srt = self.translated_srt_path.get()
            
            if not output_srt:
                lang_code = self.languages.get(self.target_language.get(), "ar")
                output_srt = input_srt.replace('.srt', f'_{lang_code}.srt')
                self.translated_srt_path.set(output_srt)
            
            target_lang = self.languages.get(self.target_language.get(), "ar")
            
            self.log_message(f"\n{'='*60}")
            self.log_message(f"🌐 بدء ترجمة: {Path(input_srt).name}")
            self.log_message(f"🎯 اللغة الهدف: {self.target_language.get()}")
            self.log_message(f"💾 الملف المترجم: {Path(output_srt).name}")
            self.log_message(f"{'='*60}")
            
            # قراءة الملف
            self.status.set("جاري قراءة الملف...")
            self.progress.set(20)
            
            with open(input_srt, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # تقسيم إلى مقاطع
            segments = content.strip().split('\n\n')
            translated_segments = []
            
            self.status.set("جاري الترجمة...")
            
            for i, segment in enumerate(segments):
                if not segment.strip():
                    continue
                    
                lines = segment.strip().split('\n')
                if len(lines) < 3:
                    translated_segments.append(segment)
                    continue
                
                # الاحتفاظ بالرقم والوقت
                segment_num = lines[0]
                time_range = lines[1]
                original_text = ' '.join(lines[2:])
                
                # تحديث التقدم
                progress_value = 20 + (i / len(segments)) * 70
                self.progress.set(int(progress_value))
                
                # ترجمة النص
                translated_text = self.translate_text(original_text, target_lang)
                
                # إعادة بناء المقطع
                translated_segments.append(f"{segment_num}\n{time_range}\n{translated_text}")
                
                # عرض التقدم
                if (i + 1) % 20 == 0:
                    self.status.set(f"جاري الترجمة... {i+1}/{len(segments)}")
                    self.log_message(f"   🔄 تم ترجمة {i+1}/{len(segments)} مقطع")
            
            # حفظ الملف المترجم
            self.status.set("جاري حفظ الملف المترجم...")
            self.progress.set(90)
            
            with open(output_srt, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(translated_segments))
            
            self.progress.set(100)
            self.status.set("اكتملت الترجمة بنجاح!")
            
            self.log_message(f"\n✅ تمت ترجمة {len(translated_segments)} مقطع بنجاح!")
            self.log_message(f"💾 الملف: {Path(output_srt).name}")
            
            # معاينة الملف المترجم
            self.preview_srt_file(output_srt)
            
            messagebox.showinfo(
                "نجاح",
                f"تمت ترجمة الملف بنجاح!\n\n"
                f"المقاطع المترجمة: {len(translated_segments)}\n"
                f"الملف: {Path(output_srt).name}"
            )
            
        except Exception as e:
            self.log_message(f"❌ خطأ في الترجمة: {str(e)}", "error")
            messagebox.showerror("خطأ", f"حدث خطأ أثناء الترجمة:\n{str(e)}")
            self.status.set("فشلت الترجمة")
        finally:
            self.is_translating = False
    
    def translate_text(self, text, target_lang="ar"):
        """ترجمة نص باستخدام Google Translate"""
        try:
            # إعداد الطلب
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'auto',  # اكتشاف تلقائي
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            query_string = urllib.parse.urlencode(params)
            full_url = f"{url}?{query_string}"
            
            # إرسال الطلب
            request = urllib.request.Request(full_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            with urllib.request.urlopen(request, timeout=10) as response:
                data = response.read().decode('utf-8')
                result = json.loads(data)
                
                # استخراج النص المترجم
                translated_parts = []
                for part in result[0]:
                    if part[0]:
                        translated_parts.append(part[0])
                
                return ' '.join(translated_parts) if translated_parts else text
                
        except Exception as e:
            self.log_message(f"⚠️ فشلت ترجمة جزء: {str(e)[:50]}", "warning")
            return text
    
    def format_time_srt(self, seconds):
        """تحويل الثواني إلى تنسيق SRT"""
        td = timedelta(seconds=seconds)
        hours = int(td.seconds // 3600)
        minutes = int((td.seconds % 3600) // 60)
        seconds_int = int(td.seconds % 60)
        milliseconds = int(td.microseconds / 1000)
        
        return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{milliseconds:03d}"
    
    def preview_srt_file(self, filepath):
        """معاينة ملف SRT"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(5000)  # قراءة أول 5000 حرف
                
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, content)
            
            # إضافة تنسيق للأرقام والأوقات
            self.preview_text.tag_config("number", foreground="#21e6c1")
            self.preview_text.tag_config("time", foreground="#e43f5a")
            
        except Exception as e:
            self.log_message(f"❌ لا يمكن معاينة الملف: {str(e)}", "error")
    
    def log_message(self, message, level="info"):
        """تسجيل رسالة في منطقة المعاينة"""
        colors = {
            "info": "#21e6c1",
            "error": "#e43f5a",
            "warning": "#ffbd39",
            "success": "#4CAF50"
        }
        
        self.preview_text.insert(tk.END, f"{message}\n")
        self.preview_text.see(tk.END)
        
        # تحديد تنسيق الرسالة
        start_index = self.preview_text.index("end-2c linestart")
        end_index = self.preview_text.index("end-1c")
        
        if level in colors:
            self.preview_text.tag_add(level, start_index, end_index)
            self.preview_text.tag_config(level, foreground=colors[level])
    
    # ========== الوظائف المساعدة ==========
    
    def quick_save(self):
        """حفظ سريع"""
        messagebox.showinfo("حفظ", "ميزة الحفظ السريع (قيد التطوير)")
    
    def save_as(self):
        """حفظ باسم"""
        messagebox.showinfo("حفظ باسم", "ميزة حفظ باسم (قيد التطوير)")
    
    def copy_text(self):
        """نسخ النص"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.preview_text.get("sel.first", "sel.last"))
    
    def paste_text(self):
        """لصق النص"""
        try:
            text = self.root.clipboard_get()
            self.preview_text.insert(tk.INSERT, text)
        except:
            pass
    
    def edit_srt(self):
        """فتح محرر SRT"""
        messagebox.showinfo("محرر SRT", "ميزة محرر SRT (قيد التطوير)")
    
    def batch_convert(self):
        """تحويل دفعة من الفيديوهات"""
        files = filedialog.askopenfilenames(
            title="اختر ملفات فيديو متعددة",
            filetypes=[("ملفات الفيديو", "*.mp4 *.avi *.mkv *.mov")]
        )
        if files:
            self.log_message(f"\n📦 بدء تحويل {len(files)} ملف...")
            # هنا يمكن إضافة كود التحويل الدفعي
            messagebox.showinfo("تحويل دفعة", f"سيتم تحويل {len(files)} ملف")
    
    def batch_translate(self):
        """ترجمة دفعة من ملفات SRT"""
        files = filedialog.askopenfilenames(
            title="اختر ملفات SRT متعددة",
            filetypes=[("ملفات SRT", "*.srt")]
        )
        if files:
            self.log_message(f"\n🌐 بدء ترجمة {len(files)} ملف...")
            messagebox.showinfo("ترجمة دفعة", f"سيتم ترجمة {len(files)} ملف")
    
    def open_settings(self):
        """فتح الإعدادات"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("الإعدادات")
        settings_window.geometry("500x400")
        settings_window.configure(bg="#162447")
        
        tk.Label(
            settings_window,
            text="⚙️ إعدادات التطبيق",
            font=("Arial", 16, "bold"),
            bg="#162447",
            fg="white"
        ).pack(pady=20)
        
        # إضافة عناصر الإعدادات هنا...
    
    def show_help(self):
        """عرض التعليمات"""
        help_text = """
        🎬 دليل استخدام مترجم SRT المتقدم
        
        📹 تحويل الفيديو إلى SRT:
        1. اختر ملف الفيديو من التبويب الأول
        2. اختر نموذج التحويل (tiny أسرع، large أدق)
        3. اضغط على "بدء تحويل الفيديو إلى SRT"
        
        🌍 ترجمة ملف SRT:
        1. اختر ملف SRT من التبويب الثاني
        2. اختر لغة المصدر واللغة الهدف
        3. اضغط على "بدء ترجمة ملف SRT"
        
        ⚙️ الأدوات المتقدمة:
        • دمج ملفات SRT
        • تقسيم ملف SRT
        • تعديل التوقيتات
        • تغيير الترميز
        
        💡 نصائح:
        - استخدم النموذج tiny للفيديوهات الطويلة
        - استخدم النموذج large لدقة أفضل
        - تأكد من اتصال الإنترنت للترجمة
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("تعليمات الاستخدام")
        help_window.geometry("600x500")
        help_window.configure(bg="#1f4068")
        
        text_widget = scrolledtext.ScrolledText(
            help_window,
            font=("Arial", 11),
            bg="#1f4068",
            fg="white",
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert(1.0, help_text)
        text_widget.config(state="disabled")
    
    def show_about(self):
        """عرض معلومات عن البرنامج"""
        about_text = """
        مترجم SRT المتقدم - الإصدار 3.0
        
        وصف:
        تطبيق متكامل لتحويل الفيديوهات إلى نصوص
        وترجمة ملفات SRT إلى لغات مختلفة
        
        الميزات:
        • تحويل الفيديو إلى SRT باستخدام Whisper
        • ترجمة ملفات SRT إلى 15 لغة
        • أدوات متقدمة لمعالجة ملفات SRT
        • واجهة عربية سهلة الاستخدام
        
        التقنيات المستخدمة:
        • OpenAI Whisper للتعرف على الصوت
        • Google Translate API للترجمة
        • Python Tkinter للواجهة الرسومية
        
        المطور: RASHEED ALRAJEHI
        
        © 2026 جميع الحقوق محفوظة
        """
        
        messagebox.showinfo("عن البرنامج", about_text)
    
    # ========== الأدوات المتقدمة ==========
    
    def merge_srt_files(self):
        """دمج ملفات SRT"""
        files = filedialog.askopenfilenames(
            title="اختر ملفات SRT للدمج",
            filetypes=[("ملفات SRT", "*.srt")]
        )
        
        if len(files) < 2:
            messagebox.showerror("خطأ", "اختر ملفين على الأقل للدمج")
            return
        
        output_file = filedialog.asksaveasfilename(
            title="حفظ الملف المدمج",
            defaultextension=".srt",
            filetypes=[("ملفات SRT", "*.srt")]
        )
        
        if output_file:
            try:
                all_segments = []
                segment_counter = 1
                
                for srt_file in files:
                    with open(srt_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    segments = content.strip().split('\n\n')
                    
                    for segment in segments:
                        if not segment.strip():
                            continue
                        
                        lines = segment.strip().split('\n')
                        if len(lines) >= 3:
                            # تحديث رقم المقطع
                            lines[0] = str(segment_counter)
                            segment_counter += 1
                            
                            # تحديث التوقيتات (هنا تحتاج منطق أكثر تعقيداً)
                            # لأجل البساطة، نتركها كما هي
                            
                            all_segments.append('\n'.join(lines))
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(all_segments))
                
                messagebox.showinfo("نجاح", f"تم دمج {len(files)} ملف بنجاح!")
                self.log_message(f"✅ تم دمج {len(files)} ملف في: {Path(output_file).name}")
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل الدمج: {str(e)}")
    
    def split_srt_file(self):
        """تقسيم ملف SRT"""
        messagebox.showinfo("تقسيم SRT", "ميزة تقسيم ملف SRT (قيد التطوير)")
    
    def adjust_timings(self):
        """تعديل توقيتات SRT"""
        messagebox.showinfo("تعديل التوقيتات", "ميزة تعديل التوقيتات (قيد التطوير)")
    
    def change_encoding(self):
        """تغيير ترميز ملف SRT"""
        filepath = filedialog.askopenfilename(
            title="اختر ملف SRT",
            filetypes=[("ملفات SRT", "*.srt")]
        )
        
        if filepath:
            encodings = ['utf-8', 'utf-16', 'windows-1256', 'iso-8859-6']
            
            encoding_window = tk.Toplevel(self.root)
            encoding_window.title("تغيير الترميز")
            encoding_window.geometry("300x200")
            encoding_window.configure(bg="#162447")
            
            tk.Label(
                encoding_window,
                text="اختر الترميز الجديد:",
                font=("Arial", 12, "bold"),
                bg="#162447",
                fg="white"
            ).pack(pady=20)
            
            selected_encoding = tk.StringVar(value="utf-8")
            
            for enc in encodings:
                tk.Radiobutton(
                    encoding_window,
                    text=enc,
                    variable=selected_encoding,
                    value=enc,
                    bg="#162447",
                    fg="white",
                    selectcolor="#162447"
                ).pack(anchor="w", padx=50)
            
            def apply_encoding():
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    new_file = filepath.replace('.srt', f'_{selected_encoding.get()}.srt')
                    
                    with open(new_file, 'w', encoding=selected_encoding.get()) as f:
                        f.write(content)
                    
                    messagebox.showinfo("نجاح", f"تم تغيير الترميز إلى {selected_encoding.get()}")
                    encoding_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل تغيير الترميز: {str(e)}")
            
            tk.Button(
                encoding_window,
                text="تطبيق",
                command=apply_encoding,
                bg="#21e6c1",
                fg="#1f4068",
                font=("Arial", 11, "bold")
            ).pack(pady=20)
    
    def extract_text_only(self):
        """استخراج النص فقط من SRT"""
        filepath = filedialog.askopenfilename(
            title="اختر ملف SRT",
            filetypes=[("ملفات SRT", "*.srt")]
        )
        
        if filepath:
            output_file = filedialog.asksaveasfilename(
                title="حفظ النص المستخرج",
                defaultextension=".txt",
                filetypes=[("ملفات نصية", "*.txt")]
            )
            
            if output_file:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    segments = content.strip().split('\n\n')
                    texts = []
                    
                    for segment in segments:
                        if not segment.strip():
                            continue
                        
                        lines = segment.strip().split('\n')
                        if len(lines) >= 3:
                            texts.append(' '.join(lines[2:]))
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(texts))
                    
                    messagebox.showinfo("نجاح", "تم استخراج النص بنجاح!")
                    self.log_message(f"📝 تم استخراج النص إلى: {Path(output_file).name}")
                    
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل استخراج النص: {str(e)}")
    
    def export_to_word(self):
        """تصدير SRT إلى مستند Word"""
        messagebox.showinfo("تصدير إلى Word", "ميزة التصدير إلى Word (قيد التطوير)")

# ========== التشغيل الرئيسي ==========

def main():
    root = tk.Tk()
    
    # تحسين شكل الواجهة
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = SRTTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()