import re
import srt
from deep_translator import GoogleTranslator
import time

def clean_html(text):
    return re.sub(r'<[^>]*>', '', text)

def arabic_numbers_to_words(text):

    time_pattern = r'(\d{1,2}):(\d{1,2}):(\d{1,2})'
    def time_repl(m):
        h, m, s = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return f"الساعة {h} ودقيقة {m} وثانية {s}"
    text = re.sub(time_pattern, time_repl, text)

    num_map = {
        '10': 'عشرة', '9': 'تسعة', '8': 'ثمانية', '7': 'سبعة', '6': 'ستة',
        '5': 'خمسة', '4': 'أربعة', '3': 'ثلاثة', '2': 'اثنان', '1': 'واحد', '0': 'صفر'
    }
    for num, word in num_map.items():
        text = re.sub(r'\b' + num + r'\b', word, text)
    
    return text

def translate_srt_file(input_path, output_path, target_lang, progress_callback=None, cancel_event=None, source_lang='auto', keep_format=True, trans_numbers=False, keep_indexes=True):
    try:
        with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
            subs = list(srt.parse(f.read()))
        
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        total = len(subs)
        translated_subs = []
        
        batch_size = 10
        for i in range(0, total, batch_size):
            if cancel_event and cancel_event.is_set():
                return False
                
            batch = subs[i:i+batch_size]
            
            texts = []
            for s in batch:
                content = s.content
                if not keep_format:
                    content = clean_html(content)
                texts.append(content)
            
            try:
                combined_text = " ||| ".join(texts)
                translated_text = None
                for attempt in range(3):
                    try:
                        translated_text = translator.translate(combined_text)
                        if translated_text: break
                    except:
                        time.sleep(2)
                
                translated_parts = translated_text.split(" ||| ")
                
                for j, part in enumerate(translated_parts):
                    if j < len(batch):
                        final_content = part.strip()
                        # خيار ترجمة الأرقام
                        if trans_numbers:
                            final_content = arabic_numbers_to_words(final_content)
                        batch[j].content = final_content
            except Exception:
                for sub in batch:
                    try:
                        content = sub.content if keep_format else clean_html(sub.content)
                        res = translator.translate(content)
                        if trans_numbers:
                            res = arabic_numbers_to_words(res)
                        sub.content = res
                    except:
                        pass
            
            translated_subs.extend(batch)
            if progress_callback:
                progress = min(100, int(((i + len(batch)) / total) * 100))
                progress_callback(progress, f"تمت ترجمة {min(i + len(batch), total)} من {total}")

        if not keep_indexes:
            for idx, sub in enumerate(translated_subs, 1):
                sub.index = idx

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt.compose(translated_subs, reindex=False))
            
        return True
    except Exception as e:
        print(f"Translation Error: {e}")
        return False
