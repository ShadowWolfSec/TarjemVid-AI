# -*- mode: python ; coding: utf-8 -*-
import os
block_cipher = None

# قائمة المكتبات التي قد لا يراها PyInstaller تلقائياً
hidden_imports = [
    'srt',
    'deep_translator',
    'docx',
    'whisper',
    'torch',
    'webview',
    'clr',
    'jinja2',
]

# تحديد المسار الحالي للمشروع
BASE_DIR = os.path.abspath(os.getcwd())
OBF_DIR = os.path.join(BASE_DIR, 'dist_obfuscated')

a = Analysis(
    [os.path.join(OBF_DIR, 'main.py')], # تشغيل الملف الأساسي المشفر
    pathex=[OBF_DIR],                  # البحث داخل مجلد التشفير
    binaries=[],
    datas=[
        ('venv/Lib/site-packages/whisper/assets', 'whisper/assets'),
        # تم إزالة ملفات structure.html و styles.css و scripts.js بنجاح لحمايتها من الاستخراج المكشوف
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# 💡 حقن الملفات المشفرة بما فيها الملف الجديد (hi) مباشرة في أرشيف البناء
extra_modules = ['audio_processor', 'hi', 'translator', 'utils']
for mod in extra_modules:
    py_path = os.path.join(OBF_DIR, f'{mod}.py')
    if os.path.exists(py_path):
        a.pure.append((mod, py_path, 'PYMODULE'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TarjemVid-AI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True, # تم تفعيلها لقص رموز المطورين وحذف بيانات الـ Debug من ملفات المكتبات والـ DLLs
    upx=True,   # لضغط حجم الملفات الثنائية وتعميتها
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False, # اتركها True حالياً لمراقبة الأخطاء في سطر الأوامر، وحولها لـ False لاحقاً لإخفاء النافذة تماماً
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='iconn.ico',
)