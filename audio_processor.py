import whisper
import os
import subprocess
import tempfile
import srt
from datetime import timedelta
import threading

class AudioProcessor:
    def __init__(self):
        self.cancel_event = threading.Event()
        self.current_process = None

    def convert_video_to_srt(self, video_path, model_name, language, progress_callback):
        self.cancel_event.clear()
        temp_audio = None
        
        try:
            progress_callback(10, "جاري استخراج الصوت من الفيديو...")
            temp_audio = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
            
            ffmpeg_cmd = [
                'ffmpeg', '-y', '-i', video_path,
                '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le',
                temp_audio
            ]
            
            self.current_process = subprocess.Popen(
                ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            
            while self.current_process.poll() is None:
                if self.cancel_event.is_set():
                    self.current_process.terminate()
                    return None
            
            if self.current_process.returncode != 0:
                raise Exception("فشل ffmpeg في استخراج الصوت")

            progress_callback(30, f"جاري تحميل نموذج Whisper ({model_name})... قد يستغرق ذلك وقتاً في المرة الأولى")
            model = whisper.load_model(model_name)
            
            if self.cancel_event.is_set(): return None

            progress_callback(50, "جاري تحليل الصوت واستخراج النصوص...")
            
            result = model.transcribe(
                temp_audio, 
                language=language if language != 'auto' else None,
                verbose=False,
                fp16=False # لضمان العمل على الأجهزة التي لا تدعم CUDA بشكل كامل
            )
            
            if self.cancel_event.is_set(): return None

            progress_callback(90, "جاري إنشاء ملف SRT...")
            subtitles = []
            for i, segment in enumerate(result['segments']):
                start = timedelta(seconds=segment['start'])
                end = timedelta(seconds=segment['end'])
                content = segment['text'].strip()
                subtitles.append(srt.Subtitle(index=i+1, start=start, end=end, content=content))
            
            progress_callback(100, "اكتملت العملية بنجاح")
            return srt.compose(subtitles)

        except Exception as e:
            print(f"Error in convert_video_to_srt: {e}")
            raise e
        finally:
            if temp_audio and os.path.exists(temp_audio):
                try: os.remove(temp_audio)
                except: pass
            self.current_process = None

    def cancel(self):
        self.cancel_event.set()
        if self.current_process:
            try: self.current_process.terminate()
            except: pass
