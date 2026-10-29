HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TarjemVid AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
        <style>
        :root {
            --primary: #00d2ff;
            --secondary: #3a7bd5;
            --bg-dark: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.7);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --accent-glow: 0 0 15px rgba(0, 210, 255, 0.4);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Cairo', 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-dark);
            background-image: radial-gradient(circle at top right, #1e293b, #0f172a);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }

        /* Glassmorphism & Navbar */
        nav {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .logo {
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(to left, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .nav-links {
            display: flex;
            gap: 20px;
            

        }


        .nav-links {
            display: flex;
            gap: 15px;
            align-items: center;
            padding: 10px;
        }

        .nav-links a {
            display: inline-block;
            padding: 10px 24px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            color: #ffffff;
            background: linear-gradient(135deg, #24292e, #2b3137); 
            border: 1px solid rgba(255, 255, 255, 0.15); 
            border-radius: 8px; /* زوايا منحنية ناعمة */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .nav-links a:hover {
            background: linear-gradient(135deg, #2b3137, #333a42); 
            color: #58a6ff; 
            border-color: #58a6ff; 
            box-shadow: 0 0 12px rgba(88, 166, 255, 0.4); 
            transform: translateY(-2px); 
        }

        .nav-links a:active {
            transform: translateY(1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .btn-donate {
            background: linear-gradient(45deg, #f59e0b, #d97706);
            padding: 8px 20px;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            font-weight: 600;
            transition: 0.3s;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        }

        .btn-donate:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5);
        }

        /* Layout */
        .container {
            display: flex;
            flex: 1;
            padding: 2rem;
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
            width: 100%;
        }

        /* Tabs Sidebar */
        .sidebar {
            width: 250px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .tab-btn {
            background: var(--card-bg);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 15px 20px;
            border-radius: 12px;
            color: var(--text-dim);
            cursor: pointer;
            text-align: right;
            transition: 0.3s;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .tab-btn i { font-size: 1.2rem; }

        .tab-btn:hover {
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
        }

        .tab-btn.active {
            background: linear-gradient(to left, var(--primary), var(--secondary));
            color: white;
            box-shadow: var(--accent-glow);
            border: none;
        }

        /* Main Content Area */
        .main-content {
            flex: 1;
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border-radius: 24px;
            padding: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            min-height: 600px;
        }

        .tab-panel {
            display: none;
            animation: fadeIn 0.4s ease;
        }

        .tab-panel.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Forms & Inputs */
        .form-group {
            margin-bottom: 1.5rem;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-dim);
            font-size: 0.9rem;
        }

        .file-picker-group {
            display: flex;
            gap: 10px;
        }

        input[type="text"], select, textarea {
            flex: 1;
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 15px;
            border-radius: 10px;
            color: white;
            outline: none;
            transition: 0.3s;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(0, 210, 255, 0.2);
        }

        .btn-action {
            background: linear-gradient(to left, var(--primary), var(--secondary));
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 700;
            transition: 0.3s;
        }

        .btn-action:hover {
            transform: scale(1.02);
            box-shadow: var(--accent-glow);
        }

        .btn-outline {
            background: transparent;
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.3s;
        }

        .btn-outline:hover { background: rgba(0, 210, 255, 0.1); }

        /* Progress Bar */
        .progress-container {
            margin-top: 2rem;
            display: none;
        }

        .progress-track {
            height: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(to left, var(--primary), var(--secondary));
            transition: width 0.3s;
            box-shadow: 0 0 10px var(--primary);
        }

        /* Logs & Preview */
        .logs-area {
            background: #000;
            border-radius: 12px;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            height: 150px;
            overflow-y: auto;
            margin-top: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .log-entry { margin-bottom: 4px; }
        .log-success { color: #10b981; }
        .log-error { color: #ef4444; }
        .log-info { color: #3b82f6; }

        .preview-area {
            margin-top: 1.5rem;
            display: none;
        }

        /* Tools Grid */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
        }

        .tool-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 1.5rem;
            border-radius: 16px;
            text-align: center;
            transition: 0.3s;
            cursor: pointer;
        }

        .tool-card:hover {
            background: rgba(255, 255, 255, 0.07);
            border-color: var(--primary);
            transform: translateY(-5px);
        }

        .tool-card i {
            font-size: 2rem;
            margin-bottom: 10px;
            display: block;
            color: var(--primary);
        }

        /* Toast Notifications */
        #toast-container {
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
        }

        .toast {
            background: var(--card-bg);
            border-right: 4px solid var(--primary);
            padding: 15px 25px;
            border-radius: 8px;
            margin-top: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            animation: slideIn 0.3s ease;
            backdrop-filter: blur(10px);
        }

        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        footer {
            padding: 2rem;
            text-align: center;
            color: var(--text-dim);
            font-size: 0.85rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Custom Checkbox Styles */
        .checkbox-container {
            display: flex;
            align-items: center;
            position: relative;
            padding-right: 35px;
            cursor: pointer;
            font-size: 0.95rem;
            user-select: none;
            color: var(--text-main);
        }

        .checkbox-container input {
            position: absolute;
            opacity: 0;
            cursor: pointer;
            height: 0;
            width: 0;
        }

        .checkmark {
            position: absolute;
            top: 0;
            right: 0;
            height: 22px;
            width: 22px;
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            transition: 0.3s;
        }

        .checkbox-container:hover input ~ .checkmark {
            background-color: rgba(255, 255, 255, 0.2);
        }

        .checkbox-container input:checked ~ .checkmark {
            background-color: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 0 10px var(--primary);
        }

        .checkmark:after {
            content: "";
            position: absolute;
            display: none;
        }

        .checkbox-container input:checked ~ .checkmark:after {
            display: block;
        }

        .checkbox-container .checkmark:after {
            left: 7px;
            top: 3px;
            width: 6px;
            height: 12px;
            border: solid white;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }

        /* Menu Bar Styles */
        .menu-bar {
            background: rgba(15, 23, 42, 0.95);
            padding: 5px 20px;
            display: flex;
            gap: 5px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.9rem;
            z-index: 1000;
        }

        .menu-item {
            position: relative;
            padding: 5px 15px;
            cursor: pointer;
            border-radius: 4px;
            transition: 0.2s;
        }

        .menu-item:hover {
            background: rgba(255, 255, 255, 0.1);
        }

        .dropdown {
            position: absolute;
            top: 100%;
            right: 0;
            background: #1e293b;
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 200px;
            border-radius: 8px;
            display: none;
            flex-direction: column;
            padding: 5px 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            backdrop-filter: blur(10px);
        }

        .menu-item:hover .dropdown {
            display: flex;
        }

        .dropdown-item {
            padding: 8px 20px;
            transition: 0.2s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .dropdown-item:hover {
            background: var(--primary);
            color: white;
        }

        .dropdown-divider {
            height: 1px;
            background: rgba(255, 255, 255, 0.05);
            margin: 5px 0;
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(5px);
            z-index: 2000;
            justify-content: center;
            align-items: center;
        }

        .modal-content {
            background: var(--bg-dark);
            padding: 2.5rem;
            border-radius: 24px;
            border: 1px solid var(--primary);
            max-width: 500px;
            width: 90%;
            text-align: center;
            position: relative;
            box-shadow: var(--accent-glow);
        }

        /* Donation modal specific (isolated) */
        .modal-overlay {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            background: rgba(0, 0, 0, 0.6) !important;
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 99999 !important;
        }

        

        /* WhatsApp button */
        .whatsapp-btn-container {
            display: inline-block !important;
            text-align: center !important;
            margin-top: 15px !important;
            font-family: sans-serif !important;
        }

        .whatsapp-btn-container .btn-whatsapp {
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            background-color: #25D366 !important;
            color: #ffffff !important;
            padding: 10px 22px !important;
            border-radius: 25px !important;
            font-size: 1rem !important;
            font-weight: bold !important;
            text-decoration: none !important;
            box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }

        .whatsapp-btn-container .btn-whatsapp:hover {
            background-color: #20ba56 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(37, 211, 102, 0.4) !important;
        }
    </style>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

<div class="menu-bar">
    <div class="menu-item">
        ملف
        <div class="dropdown">
            <div class="dropdown-item" onclick="selectFile('video')">فتح فيديو <span>Ctrl+O</span></div>
            <div class="dropdown-item" onclick="selectFile('srt')">فتح ملف ترجمة</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="savePreview()">حفظ</div>
            <div class="dropdown-item" onclick="savePreview()">حفظ باسم...</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="window.close()">خروج</div>
        </div>
    </div>
    <div class="menu-item">
        تحرير
        <div class="dropdown">
            <div class="dropdown-item" onclick="editAction('copy')">نسخ</div>
            <div class="dropdown-item" onclick="editAction('paste')">لصق</div>
            <div class="dropdown-item" onclick="editAction('selectAll')">تحديد الكل</div>
            <div class="dropdown-item" onclick="editAction('clear')">مسح</div>
        </div>
    </div>
    <div class="menu-item">
        أدوات
        <div class="dropdown">
            <div class="dropdown-item" onclick="batchAction('convert_files')">تحويل ملفات متعددة...</div>
            <div class="dropdown-item" onclick="batchAction('convert_folder')">تحويل مجلد كامل...</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="batchAction('translate_files')">ترجمة ملفات متعددة...</div>
            <div class="dropdown-item" onclick="batchAction('translate_folder')">ترجمة مجلد كامل...</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="batchAction('mergeFolder')">دمج مجلد كامل...</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="showTab('settings')">الإعدادات</div>
        </div>
    </div>
    <div class="menu-item">
        مساعدة
        <div class="dropdown">
            <div class="dropdown-item" onclick="showModal('about')">عن البرنامج</div>
            <div class="dropdown-item" onclick="showModal('help')">التعليمات</div>
            <div class="dropdown-divider"></div>
            <div class="dropdown-item" onclick="showModal('dev')">المطور</div>
        </div>
    </div>
</div>

<nav>
    <div class="logo">
        TarjemVid-AI
    </div>
    <div class="nav-links">
        <a href="https://github.com/ShadowWolfSec" target="_blank">GitHub</a>

    </div>
</nav>



<div class="container">
    <div class="sidebar">
        <div class="tab-btn active" onclick="showTab('transcribe')">
            <i>🎙️</i> استخراج النصوص
        </div>
        <div class="tab-btn" onclick="showTab('translate')">
            <i>🌍</i> ترجمة SRT
        </div>
         <div class="tab-btn" onclick="showTab('tools')"> 
            <i>🛠️</i> أدوات متقدمة
        </div>
        <div class="tab-btn" onclick="showTab('settings')">
            <i>⚙️</i> الإعدادات
        </div>
    </div>

    <div class="main-content">
        <!-- Transcribe Panel -->
        <div id="transcribe" class="tab-panel active">
            <h2 style="margin-bottom: 1.5rem;">استخراج النصوص من الفيديو</h2>
            <div class="form-group">
                <label>اختر ملف الفيديو:</label>
                <div class="file-picker-group">
                    <input type="text" id="video-path" placeholder="لم يتم اختيار ملف..." readonly>
                    <button class="btn-outline" onclick="selectFile('video')">اختيار</button>
                </div>
            </div>
            <div class="form-group">
                <label>حدد مكان حفظ ملف SRT الناتج:</label>
                <div class="file-picker-group">
                    <input type="text" id="transcribe-save-path" placeholder="سيتم الحفظ تلقائياً بجانب الفيديو إذا ترك فارغاً..." readonly>
                    <button class="btn-outline" onclick="selectSavePath('srt', 'transcribe-save-path')">تحديد المسار</button>
                </div>
            </div>
            <div style="display: flex; gap: 1rem;">
                <div class="form-group" style="flex: 1;">
                    <label>نموذج Whisper:</label>
                    <select id="whisper-model">
                        <option value="tiny">Tiny (الأسرع)</option>
                        <option value="base">Base (متوازن)</option>
                        <option value="small" selected>Small (جيد جداً)</option>
                        <option value="medium">Medium (دقة عالية)</option>
                        <option value="large">Large (الأفضل - ثقيل)</option>
                    </select>
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>لغة الفيديو:</label>
                    <select id="video-lang">
                        <option value="auto">تعرف تلقائي</option>
                        <option value="ar">العربية</option>
                        <option value="en">الإنجليزية</option>
                        <option value="fr">الفرنسية</option>
                        <option value="de">الألمانية</option>
                        <option value="es">الإسبانية</option>
                        <option value="tr">التركية</option>
                        <option value="it">الإيطالية</option>
                        <option value="ru">الروسية</option>
                        <option value="zh">الصينية</option>
                        <option value="ja">اليابانية</option>
                        <option value="ko">الكورية</option>
                        <option value="fa">الفارسية</option>
                        <option value="hi">الهندية</option>
                        <option value="nl">الهولندية</option>
                        <option value="pt">البرتغالية</option>
                    </select>
                </div>
            </div>
            <button class="btn-action" id="btn-start-transcribe" onclick="startTranscription()">بدء الاستخراج</button>
            <button class="btn-action cancel-btn" id="btn-cancel-transcribe" onclick="cancelOperation()">إلغاء العملية</button>
        </div>

        <!-- Translate Panel -->
        <div id="translate" class="tab-panel">
            <h2 style="margin-bottom: 1.5rem;">ترجمة ملفات SRT</h2>
            <div class="form-group">
                <label>اختر ملف SRT:</label>
                <div class="file-picker-group">
                    <input type="text" id="srt-path" placeholder="لم يتم اختيار ملف..." readonly>
                    <button class="btn-outline" onclick="selectFile('srt')">اختيار</button>
                </div>
            </div>
            <div class="form-group" style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-top: 10px;">
                <label style="margin-bottom: 10px; color: var(--primary); font-weight: bold;">خيارات الترجمة المتقدمة:</label>
                <div style="display: flex; flex-direction: column; gap: 10px;">
                    <label class="checkbox-container">
                        <input type="checkbox" id="keep-format" checked>
                        <span class="checkmark"></span>
                        📄 الحفاظ على التنسيق الأصلي
                    </label>
                    <label class="checkbox-container">
                        <input type="checkbox" id="trans-numbers">
                        <span class="checkmark"></span>
                        🔢 ترجمة الأرقام والتوقيتات
                    </label>
                    <label class="checkbox-container">
                        <input type="checkbox" id="keep-indexes" checked>
                        <span class="checkmark"></span>
                        🔢 الحفاظ على أرقام التسلسل الأصلية
                    </label>
                </div>
            </div>
            <div class="form-group">
                <label>حدد مكان حفظ الملف المترجم:</label>
                <div class="file-picker-group">
                    <input type="text" id="translate-save-path" placeholder="سيتم إضافة اسم اللغة للملف إذا ترك فارغاً..." readonly>
                    <button class="btn-outline" onclick="selectSavePath('srt', 'translate-save-path')">تحديد المسار</button>
                </div>
            </div>
            <div style="display: flex; gap: 1rem;">
                <div class="form-group" style="flex: 1;">
                    <label>لغة المصدر:</label>
                    <select id="source-lang">
                        <option value="auto">تعرف تلقائي</option>
                        <option value="ar">العربية</option>
                        <option value="en">الإنجليزية</option>
                        <option value="fr">الفرنسية</option>
                        <option value="de">الألمانية</option>
                        <option value="es">الإسبانية</option>
                        <option value="tr">التركية</option>
                        <option value="it">الإيطالية</option>
                        <option value="ru">الروسية</option>
                        <option value="zh">الصينية</option>
                        <option value="ja">اليابانية</option>
                        <option value="ko">الكورية</option>
                        <option value="fa">الفارسية</option>
                        <option value="hi">الهندية</option>
                        <option value="nl">الهولندية</option>
                        <option value="pt">البرتغالية</option>
                    </select>
                </div>
                <div class="form-group" style="flex: 1;">
                    <label>اللغة الهدف:</label>
                    <select id="target-lang">
                        <option value="ar">العربية</option>
                        <option value="en">الإنجليزية</option>
                        <option value="fr">الفرنسية</option>
                        <option value="de">الألمانية</option>
                        <option value="es">الإسبانية</option>
                        <option value="tr">التركية</option>
                        <option value="it">الإيطالية</option>
                        <option value="ru">الروسية</option>
                        <option value="zh">الصينية</option>
                        <option value="ja">اليابانية</option>
                        <option value="ko">الكورية</option>
                        <option value="fa">الفارسية</option>
                        <option value="hi">الهندية</option>
                        <option value="nl">الهولندية</option>
                        <option value="pt">البرتغالية</option>
                    </select>
                </div>
            </div>
            <button class="btn-action" id="btn-start-translate" onclick="startTranslation()">بدء الترجمة</button>
            <button class="btn-action cancel-btn" id="btn-cancel-translate" onclick="cancelOperation()">إلغاء العملية</button>
        </div>
        <!-- Tools Panel -->
        <div id="tools" class="tab-panel">
            <h2 style="margin-bottom: 1.5rem;">الأدوات المتقدمة</h2>
            <div class="tools-grid">
                <div class="tool-card" onclick="toolAction('merge')">
                    <i>🔗</i>
                    <h3>دمج ملفات</h3>
                    <p>دمج عدة ملفات SRT</p>
                </div>
                <div class="tool-card" onclick="toolAction('split')">
                    <i>✂️</i>
                    <h3>تقسيم SRT</h3>
                    <p>تقسيم حسب الثواني</p>
                </div>
                <div class="tool-card" onclick="toolAction('adjust')">
                    <i>⏱️</i>
                    <h3>تعديل التوقيت</h3>
                    <p>تقديم أو تأخير</p>
                </div>
                <div class="tool-card" onclick="toolAction('encoding')">
                    <i>🔤</i>
                    <h3>تغيير الترميز</h3>
                    <p>إصلاح الرموز الغريبة</p>
                </div>
                <div class="tool-card" onclick="toolAction('rawtext')">
                    <i>📄</i>
                    <h3>نص خام</h3>
                    <p>استخراج النص فقط</p>
                </div>
                <div class="tool-card" onclick="toolAction('word')">
                    <i>📝</i>
                    <h3>تصدير Word</h3>
                    <p>تحويل لملف منسق</p>
                </div>
            </div>
        </div>        
        <!-- Settings Panel (مخفي حاليًا) -->
        <div id="settings" class="tab-panel">
            <h2 style="margin-bottom: 2rem;">الإعدادات العامة</h2>
            <div class="form-group">
                <label>اللغة الافتراضية للترجمة:</label>
                <select id="default-lang" onchange="updateSettings()">
                    <option value="ar">العربية</option>
                    <option value="en">الإنجليزية</option>
                    <option value="fr">الفرنسية</option>
                </select>
            </div>
            <div class="form-group">
                <label>نموذج Whisper الافتراضي:</label>
                <select id="default-model" onchange="updateSettings()">
                    <option value="tiny">Tiny (الأسرع)</option>
                    <option value="base">Base</option>
                    <option value="small">Small</option>
                    <option value="medium">Medium</option>
                </select>
            </div>
            <p style="color: var(--text-dim); margin-top: 1rem;">يتم حفظ الإعدادات تلقائياً عند تغييرها.</p>
        </div>

        <!-- Progress and Logs -->
        <div class="progress-container" id="progress-container">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span id="progress-status">جاري المعالجة...</span>
                <span id="progress-percent">0%</span>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
        </div>

        <div class="logs-area" id="logs-area">
            <div class="log-entry log-info">مرحباً بك في TarjemVid-AI... جاهز للعمل.</div>
        </div>
        
        <div class="preview-area" id="preview-area">
            <h3>معاينة النتائج:</h3>
            <textarea id="srt-preview" style="width: 100%; height: 200px; margin-top: 10px;"></textarea>
            <button class="btn-action" style="margin-top: 10px;" onclick="savePreview()">حفظ التعديلات</button>
        </div>
    </div>
</div>

<div id="modal-container" class="modal" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <h2 id="modal-title" style="color: var(--primary); margin-bottom: 1rem;"></h2>
        <div id="modal-body" style="line-height: 1.6; color: var(--text-main);"></div>
        <button class="btn-outline" style="margin-top: 2rem;" onclick="closeModal()">إغلاق</button>
    </div>
</div>

<div id="toast-container"></div>

<footer>
    TarjemVid-AI v2.0 &copy; 2026 | Developer BY : ENG RASHEED AL-RAJEHI
</footer>

<script>
         function showModal(type) {
        const container = document.getElementById('modal-container');
        const title = document.getElementById('modal-title');
        const body = document.getElementById('modal-body');
        
        if (type === 'dev') {
            title.innerText = 'معلومات المطور';
            body.innerHTML = `
                <p>تم تطوير هذا البرنامج بواسطة:</p>
                <h3 style="margin: 10px 0;">المهندس:رشيد الراجحي</h3>
                <p>للتواصل والاستفسارات عبر واتساب:</p>
                <div class="whatsapp-btn-container">
                    <a href="https://wa.me/9677?text=استفسار" target="_blank" class="btn-whatsapp">
                        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.563 7.93-7.93a7.9 7.9 0 0 0-2.327-5.607zm-5.604 11.948a6.51 6.51 0 0 1-3.305-.904l-.237-.14-2.456.644.656-2.396-.153-.244a6.51 6.51 0 0 1-1.006-3.506c.003-3.593 2.922-6.513 6.516-6.513a6.51 6.51 0 0 1 4.58 1.916 6.51 6.51 0 0 1 1.914 4.59c-.004 3.593-2.923 6.513-6.52 6.513zm3.623-4.937c-.198-.1-.1.198-.519-.395-.316-.2-.612-.112-.663-.138-.052-.025-.316-.123-.613-.393-.23-.21-.384-.469-.43-.548-.047-.08-.005-.122.035-.161.036-.035.08-.09.12-.137.04-.047.052-.08.08-.13.027-.053.013-.1-.002-.132-.015-.033-.137-.33-.189-.452-.05-.124-.102-.107-.138-.109-.03-.002-.066-.002-.104-.002-.039 0-.102.015-.155.072-.053.058-.201.197-.201.48 0 .284.207.558.236.596.029.038.407.621.986.872.138.06.246.095.33.122.14.044.267.038.368.023.111-.016.343-.14.392-.275.049-.135.049-.251.034-.275-.015-.024-.055-.038-.253-.137z"/>
                        </svg>
                        تواصل عبر واتساب
                    </a>
                </div>
                <p style="margin-top: 10px;">تمنى أن ينال البرنامج إعجابكم!</p>
            `;
        } else if (type === 'about') {
            title.innerText = 'عن TarjemVid-AI';
            body.innerHTML = `
                <p>TarjemVid-AI هو أداة لمعالجة وترجمة ملفات الترجمة (SRT) واستخراج النصوص من الفيديوهات باستخدام تقنيات الذكاء الاصطناعي (Whisper).</p>
                <p style="margin-top: 10px;">الإصدار: 2.0</p>
            `;
        } else if (type === 'help') {
            title.innerText = 'التعليمات';
            body.innerHTML = `
                <ul style="text-align: right; display: inline-block;">
                    <li>اختر فيديو من تبويب "استخراج" للبدء.</li>
                    <li>استخدم تبويب "ترجمة" لترجمة ملفات SRT.</li>
                    <li>تأكد من وجود اتصال بالإنترنت للترجمة.</li>
                    <li>يمكنك تعديل الملفات يدوياً في منطقة المعاينة.</li>
                </ul>
            `;
        }
        container.style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('modal-container').style.display = 'none';
    }

    function editAction(action) {
        const preview = document.getElementById('srt-preview');
        preview.focus();
        if (action === 'copy') document.execCommand('copy');
        else if (action === 'paste') navigator.clipboard.readText().then(t => preview.value += t);
        else if (action === 'selectAll') preview.select();
        else if (action === 'clear') preview.value = '';
    }

    async function batchAction(type) {
        const options = {
            keepFormat: document.getElementById('keep-format').checked,
            transNumbers: document.getElementById('trans-numbers').checked,
            keepIndexes: document.getElementById('keep-indexes').checked
        };

        if (type === 'convert_files') {
            const files = await pywebview.api.select_files(['فيديو (*.mp4;*.mkv;*.avi;*.mov)']);
            if (files) await pywebview.api.batch_process_files(files, 'convert', options);
        } else if (type === 'convert_folder') {
            const folder = await pywebview.api.select_folder();
            if (folder) await pywebview.api.batch_process_folder(folder, 'convert', options);
        } else if (type === 'translate_files') {
            const files = await pywebview.api.select_files(['ترجمة (*.srt)']);
            if (files) await pywebview.api.batch_process_files(files, 'translate', options);
        } else if (type === 'translate_folder') {
            const folder = await pywebview.api.select_folder();
            if (folder) await pywebview.api.batch_process_folder(folder, 'translate', options);
        } else if (type === 'mergeFolder') {
            const folder = await pywebview.api.select_folder();
            if (folder) await pywebview.api.merge_folder(folder);
        }
    }

    async function updateSettings() {
        const settings = {
            model: document.getElementById('default-model').value,
            lang: document.getElementById('default-lang').value
        };
        await pywebview.api.save_settings(settings);
        showToast('تم حفظ الإعدادات', 'success');
    }

    function showTab(tabId) {
        document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(tabId).classList.add('active');
        event.currentTarget.classList.add('active');
    }

    function showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.style.borderRightColor = type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#00d2ff';
        toast.innerText = message;
        container.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    function updateLog(message, type = 'info') {
        const logs = document.getElementById('logs-area');
        const entry = document.createElement('div');
        entry.className = `log-entry log-${type}`;
        entry.innerText = `[${new Date().toLocaleTimeString()}] ${message}`;
        logs.appendChild(entry);
        logs.scrollTop = logs.scrollHeight;
    }

    function updateProgress(percent, status) {
        const container = document.getElementById('progress-container');
        container.style.display = 'block';
        document.getElementById('progress-fill').style.width = percent + '%';
        document.getElementById('progress-percent').innerText = percent + '%';
        document.getElementById('progress-status').innerText = status;
        updateLog(status);
    }

    // ====================== استدعاءات Python ======================
    async function selectFile(type) {
        let fileTypes = [];
        if (type === 'video') fileTypes = ['فيديو (*.mp4;*.mkv;*.avi;*.mov)', 'جميع الملفات (*.*)'];
        else if (type === 'srt') fileTypes = ['ترجمة (*.srt)', 'جميع الملفات (*.*)'];
        
        const path = await pywebview.api.select_file(fileTypes);
        if (path) {
            if (type === 'video') document.getElementById('video-path').value = path;
            else document.getElementById('srt-path').value = path;
            updateLog(`تم اختيار الملف: ${path}`);
        }
    }

    async function selectSavePath(ext, targetId) {
        const path = await pywebview.api.save_file_dialog("حدد مكان الحفظ", "." + ext);
        if (path) {
            document.getElementById(targetId).value = path;
            updateLog(`تم تحديد مسار الحفظ: ${path}`);
        }
    }

    async function startTranscription() {
        const path = document.getElementById('video-path').value;
        const savePath = document.getElementById('transcribe-save-path').value;
        const model = document.getElementById('whisper-model').value;
        const lang = document.getElementById('video-lang').value;

        if (!path) return showToast('يرجى اختيار ملف فيديو أولاً', 'error');

        document.getElementById('btn-start-transcribe').style.display = 'none';

        updateProgress(5, 'بدء عملية الاستخراج...');
        const result = await pywebview.api.convert_video(path, model, lang, savePath);
        
        if (result) {
            document.getElementById('preview-area').style.display = 'block';
            document.getElementById('srt-preview').value = result;
            showToast('تم استخراج النصوص بنجاح', 'success');
        }
        
        document.getElementById('btn-start-transcribe').style.display = 'inline-block';
    }

    async function startTranslation() {
        const path = document.getElementById('srt-path').value;
        const savePath = document.getElementById('translate-save-path').value;
        const sourceLang = document.getElementById('source-lang').value;
        const targetLang = document.getElementById('target-lang').value;
        
        const options = {
            keepFormat: document.getElementById('keep-format').checked,
            transNumbers: document.getElementById('trans-numbers').checked,
            keepIndexes: document.getElementById('keep-indexes').checked
        };

        if (!path) return showToast('يرجى اختيار ملف SRT أولاً', 'error');

        document.getElementById('btn-start-translate').style.display = 'none';

        updateProgress(5, 'بدء عملية الترجمة...');
        const success = await pywebview.api.translate_srt(path, targetLang, savePath, sourceLang, options);
        
        if (success) showToast('تمت الترجمة بنجاح وتم حفظ الملف', 'success');
        else showToast('فشلت عملية الترجمة أو تم إلغاؤها', 'error');

        document.getElementById('btn-start-translate').style.display = 'inline-block';
    }

    async function cancelOperation() {
        await pywebview.api.cancel_operation();
        showToast('تم إلغاء العملية', 'info');
        document.getElementById('progress-container').style.display = 'none';
        // إعادة إظهار أزرار البدء في حال كانت مخفية
        document.getElementById('btn-start-transcribe').style.display = 'inline-block';
        document.getElementById('btn-start-translate').style.display = 'inline-block';
    }

    async function toolAction(action) {
        const srtPath = document.getElementById('srt-path').value || document.getElementById('video-path').value;
        
        if (action === 'merge') {
            const files = await pywebview.api.select_files(['ملفات SRT (*.srt)']);
            if (files) await pywebview.api.merge_srt(files);
        } else if (action === 'split') {
            if (!srtPath) return showToast('اختر ملفاً أولاً', 'error');
            const seconds = prompt('أدخل عدد الثواني للتقسيم:', '300');
            if (seconds) await pywebview.api.split_srt(srtPath, seconds);
        } else if (action === 'adjust') {
            if (!srtPath) return showToast('اختر ملفاً أولاً', 'error');
            const delta = prompt('أدخل فارق التوقيت بالثواني (مثال: 1.5 أو -2.0):', '1.0');
            if (delta) await pywebview.api.adjust_time(srtPath, delta);
        } else if (action === 'encoding') {
            if (!srtPath) return showToast('اختر ملفاً أولاً', 'error');
            await pywebview.api.change_encoding(srtPath);
        } else if (action === 'rawtext') {
            if (!srtPath) return showToast('اختر ملفاً أولاً', 'error');
            await pywebview.api.extract_text(srtPath);
        } else if (action === 'word') {
            if (!srtPath) return showToast('اختر ملفاً أولاً', 'error');
            await pywebview.api.export_word(srtPath);
        }
    }

    async function savePreview() {
        const content = document.getElementById('srt-preview').value;
        const success = await pywebview.api.save_srt_content(content);
        if (success) showToast('تم حفظ التغييرات', 'success');
    }

    document.addEventListener('DOMContentLoaded', function() {
        const cancelTranscribe = document.getElementById('btn-cancel-transcribe');
        const cancelTranslate = document.getElementById('btn-cancel-translate');
        if (cancelTranscribe) cancelTranscribe.style.display = 'inline-block';
        if (cancelTranslate) cancelTranslate.style.display = 'inline-block';
    });
</script>

</body>
</html>
"""
