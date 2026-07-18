function openDonateModal(e) {
    e.preventDefault();
    document.getElementById('donateModal').style.display = 'flex';
}

function closeDonateModal() {
    document.getElementById('donateModal').style.display = 'none';
}

window.onclick = function(event) {
    var modal = document.getElementById('donateModal');
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

function showModal(type) {
    const container = document.getElementById('modal-container');
    const title = document.getElementById('modal-title');
    const body = document.getElementById('modal-body');
    
    if (type === 'dev') {
        title.innerText = 'معلومات المطور';
        body.innerHTML = `
            <p>تم تطوير هذا البرنامج بواسطة:</p>
            <h3 style="margin: 10px 0;">المهندس: رشيد الراجحي</h3>
            <p>للتواصل والاستفسارات عبر واتساب:</p>
            <div class="whatsapp-btn-container">
                <a href="https://wa.me/967771510536?text=استفسار" target="_blank" class="btn-whatsapp">
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
            <p>TarjemVid-AI هو أداة احترافية لمعالجة وترجمة ملفات الترجمة (SRT) واستخراج النصوص من الفيديوهات باستخدام تقنيات الذكاء الاصطناعي (Whisper).</p>
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

async function updateSettings() {
    const settings = {
        model: document.getElementById('default-model').value,
        lang: document.getElementById('default-lang').value
    };
    if (typeof pywebview !== 'undefined' && pywebview.api) {
        await pywebview.api.save_settings(settings);
    }
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

// Python Bridge Calls (محاكاة للعرض، يمكن ربطها مع pywebview)
async function selectFile(type) {
    let fileTypes = [];
    if (type === 'video') fileTypes = ['فيديو (*.mp4;*.mkv;*.avi;*.mov)', 'جميع الملفات (*.*)'];
    else if (type === 'srt') fileTypes = ['ترجمة (*.srt)', 'جميع الملفات (*.*)'];
    
    // محاكاة اختيار ملف (في التطبيق الحقيقي يتم استدعاء pywebview)
    const fakePath = type === 'video' ? 'C:/videos/sample.mp4' : 'C:/subtitles/subtitle.srt';
    if (type === 'video') document.getElementById('video-path').value = fakePath;
    else document.getElementById('srt-path').value = fakePath;
    updateLog(`تم اختيار الملف: ${fakePath}`);
    showToast(`تم اختيار الملف: ${fakePath.split('/').pop()}`, 'success');
}

async function selectSavePath(ext, targetId) {
    const fakePath = `C:/output/file.${ext}`;
    document.getElementById(targetId).value = fakePath;
    updateLog(`تم تحديد مسار الحفظ: ${fakePath}`);
    showToast('تم تحديد مسار الحفظ', 'success');
}

async function startTranscription() {
    const path = document.getElementById('video-path').value;
    if (!path) return showToast('يرجى اختيار ملف فيديو أولاً', 'error');

    document.getElementById('btn-start-transcribe').style.display = 'none';
    document.getElementById('btn-cancel-transcribe').style.display = 'inline-block';
    
    updateProgress(5, 'بدء عملية الاستخراج...');
    
    // محاكاة العملية
    let percent = 0;
    const interval = setInterval(() => {
        percent += 10;
        if (percent <= 100) {
            updateProgress(percent, `جاري استخراج النصوص... ${percent}%`);
        }
        if (percent >= 100) {
            clearInterval(interval);
            const fakeResult = `1\n00:00:01,000 --> 00:00:05,000\nهذا نص تجريبي للترجمة\n\n2\n00:00:06,000 --> 00:00:10,000\nنص تجريبي آخر`;
            document.getElementById('preview-area').style.display = 'block';
            document.getElementById('srt-preview').value = fakeResult;
            showToast('تم استخراج النصوص بنجاح', 'success');
            updateLog('اكتمل استخراج النصوص بنجاح', 'success');
            document.getElementById('btn-start-transcribe').style.display = 'inline-block';
            document.getElementById('btn-cancel-transcribe').style.display = 'none';
            document.getElementById('progress-container').style.display = 'none';
        }
    }, 500);
}

async function startTranslation() {
    const path = document.getElementById('srt-path').value;
    if (!path) return showToast('يرجى اختيار ملف SRT أولاً', 'error');

    document.getElementById('btn-start-translate').style.display = 'none';
    document.getElementById('btn-cancel-translate').style.display = 'inline-block';

    updateProgress(5, 'بدء عملية الترجمة...');
    
    // محاكاة العملية
    let percent = 0;
    const interval = setInterval(() => {
        percent += 10;
        if (percent <= 100) {
            updateProgress(percent, `جاري الترجمة... ${percent}%`);
        }
        if (percent >= 100) {
            clearInterval(interval);
            showToast('تمت الترجمة بنجاح وتم حفظ الملف', 'success');
            updateLog('اكتملت الترجمة بنجاح', 'success');
            document.getElementById('btn-start-translate').style.display = 'inline-block';
            document.getElementById('btn-cancel-translate').style.display = 'none';
            document.getElementById('progress-container').style.display = 'none';
        }
    }, 500);
}

async function cancelOperation() {
    showToast('تم إلغاء العملية', 'info');
    document.getElementById('progress-container').style.display = 'none';
    document.getElementById('btn-start-transcribe').style.display = 'inline-block';
    document.getElementById('btn-cancel-transcribe').style.display = 'none';
    document.getElementById('btn-start-translate').style.display = 'inline-block';
    document.getElementById('btn-cancel-translate').style.display = 'none';
}

async function savePreview() {
    const content = document.getElementById('srt-preview').value;
    showToast('تم حفظ التغييرات (محاكاة)', 'success');
    updateLog('تم حفظ محتوى المعاينة', 'success');
}