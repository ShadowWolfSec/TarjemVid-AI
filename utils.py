import srt
from docx import Document
import os
import chardet
from datetime import timedelta

def merge_srt_files(file_paths, output_path):
    """دمج عدة ملفات SRT في ملف واحد مع الحفاظ على الترتيب"""
    all_subtitles = []
    current_time_offset = timedelta(0)
    
    for path in file_paths:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            subs = list(srt.parse(f.read()))
            if subs:
                # نعدل أرقام التسلسل والتوقيتات لتكون متتابعة
                for s in subs:
                    s.start += current_time_offset
                    s.end += current_time_offset
                all_subtitles.extend(subs)
                current_time_offset = subs[-1].end + timedelta(seconds=1)
                
    # إعادة ترقيم التسلسل
    for i, sub in enumerate(all_subtitles):
        sub.index = i + 1
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(all_subtitles))
    return True

def split_srt_by_seconds(file_path, seconds, output_prefix):
    """تقسيم ملف SRT إلى أجزاء بناءً على عدد الثواني"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        subs = list(srt.parse(f.read()))
        
    split_duration = timedelta(seconds=seconds)
    current_part = []
    part_index = 1
    start_time = subs[0].start
    
    for sub in subs:
        if sub.start - start_time > split_duration:
            # حفظ الجزء الحالي
            output_path = f"{output_prefix}_part{part_index}.srt"
            with open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(srt.compose(current_part))
            
            # بدء جزء جديد
            current_part = []
            part_index += 1
            start_time = sub.start
            
        current_part.append(sub)
        
    # حفظ الجزء الأخير
    if current_part:
        output_path = f"{output_prefix}_part{part_index}.srt"
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.write(srt.compose(current_part))
    return True

def adjust_srt_timing(file_path, output_path, seconds_delta):
    """تعديل توقيت الترجمة بالتقديم أو التأخير"""
    delta = timedelta(seconds=float(seconds_delta))
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        subs = list(srt.parse(f.read()))
        
    for sub in subs:
        sub.start += delta
        sub.end += delta
        if sub.start < timedelta(0): sub.start = timedelta(0)
        if sub.end < timedelta(0): sub.end = timedelta(0)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt.compose(subs))
    return True

def change_srt_encoding(file_path, output_path, to_enc='utf-8'):
    """تغيير ترميز ملف SRT"""
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        from_enc = detected['encoding']
        
    content = raw_data.decode(from_enc, errors='ignore')
    with open(output_path, 'w', encoding=to_enc) as f:
        f.write(content)
    return True

def extract_raw_text(file_path, output_path):
    """استخراج النص فقط من ملف SRT بدون أرقام أو توقيتات"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        subs = list(srt.parse(f.read()))
        
    text_only = [sub.content.replace('\n', ' ') for sub in subs]
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(text_only))
    return True

def export_to_word(file_path, output_path):
    """تصدير محتوى SRT إلى ملف Word منسق"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        subs = list(srt.parse(f.read()))
        
    doc = Document()
    doc.add_heading('TarjemVid Pro - SRT Export', 0)
    
    table = doc.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = '#'
    hdr_cells[1].text = 'Timing'
    hdr_cells[2].text = 'Text'
    
    for sub in subs:
        row_cells = table.add_row().cells
        row_cells[0].text = str(sub.index)
        row_cells[1].text = f"{srt.timedelta_to_srt_timestamp(sub.start)} --> {srt.timedelta_to_srt_timestamp(sub.end)}"
        row_cells[2].text = sub.content
        
    doc.save(output_path)
    return True
def parse_srt_blocks(file_path):
    """تحليل ملف SRT إلى كتل برمجية"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return list(srt.parse(f.read()))

def rebuild_srt(subtitles):
    """إعادة بناء نص SRT من قائمة الكتل"""
    return srt.compose(subtitles)
