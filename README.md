# TarjemVid-AI

**AI-powered video transcription, subtitle translation, and SRT tools.**  

TarjemVid-AI is a desktop application for transcribing video and working with subtitle files. It uses **OpenAI Whisper** for speech recognition. Transcription can run offline after the required model is downloaded; subtitle translation requires an internet connection.

### Features

- **Transcription:** Whisper models Tiny, Base, Small, Medium, and Large; automatic or manual language selection; SRT export; support for 15+ languages.
- **SRT translation:** Single-file and batch translation, optional preservation of HTML formatting and sequence numbers, optional conversion of numbers and timestamps to Arabic words, and up to three automatic retries on failure.
- **Subtitle tools:** Merge files with timing recalculation, split files, shift subtitle timing, convert encoding to UTF-8, extract plain text, and export to Word.
- **Batch processing:** Transcribe multiple videos, translate multiple SRT files, or process a folder.

### Requirements

- Python 3.11 
- FFmpeg
- Dependencies in `requirements.txt`

Install FFmpeg using your operating system's package manager. For Ubuntu/Debian and macOS:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

On Windows, download an FFmpeg build (the ZIP package containing `ffmpeg.exe`), extract it to a permanent location such as `C:\ffmpeg`, then add the `bin` folder (for example, `C:\ffmpeg\bin`) to the Windows `PATH` environment variable. Add the folder, not the `ffmpeg.exe` file itself. Open a new terminal and verify the installation:

```bash
ffmpeg -version
```

### Install and Run

```bash
git clone https://github.com/ShadowWolfSec/TarjemVid-AI.git
cd TarjemVid-AI

# Optional, recommended: create a virtual environment
python -m venv venv

# Activate it — Windows:
venv\Scripts\activate
# Activate it — Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
python main.py
```

### Basic Usage

**Transcribe a video:** Open the transcription tab, select a video and a Whisper model, choose a language or automatic detection, then start transcription. The subtitles are exported as an SRT file.

**Translate subtitles:** Open the SRT translation tab, select a file, choose the source and target languages and any desired options, then start translation. An internet connection is required.

**Use subtitle tools:** Open the advanced tools tab, choose an operation (merge, split, timing adjustment, encoding conversion, text extraction, or Word export), and follow the on-screen instructions.

### Whisper Models

Models are normally downloaded automatically on first use and cached under `~/.cache/whisper/` (on Windows: `%USERPROFILE%\.cache\whisper\`). An internet connection is required for the initial download. Approximate sizes:

| Model | Size | Summary |
|---|---:|---|
| Tiny | 39 MB | Fastest; comparatively lower accuracy |
| Base | 74 MB | Balanced |
| Small | 244 MB | Higher accuracy; moderate resource use |
| Medium | 769 MB | High accuracy; greater resource use |
| Large | 1.5 GB | Highest accuracy of the listed options; most resource-intensive |

If automatic download fails, download the compatible Whisper checkpoint for the selected model and place it in the cache folder above. Keep the checkpoint's expected filename (for example, `Tiny.pt` for the Tiny model). Use a genuine OpenAI Whisper checkpoint; files named `pytorch_model.bin` from other model formats may not be compatible. Restart the application and select the model again.

### Project Structure

```text
TarjemVid-AI/
├── main.py              # Application entry point
├── gui.py               # User interface (HTML/CSS/JavaScript)
├── audio_processor.py   # Audio processing and Whisper transcription
├── translator.py        # Subtitle translation
├── utils.py             # SRT processing utilities
├── requirements.txt     # Python dependencies
├── settings.json        # Application settings
└── README.md
```

### Technologies

`pywebview` (desktop interface) · `openai-whisper` and `torch` (speech recognition) · `deep-translator` (online translation) · `srt` (subtitle processing) · `python-docx` (Word export) · `ffmpeg-python` (FFmpeg integration)

### Troubleshooting

- **FFmpeg not found (Windows):** Confirm that the folder containing `ffmpeg.exe` (usually `bin`) is in `PATH`, then open a new terminal and run `ffmpeg -version`.
- **Model download fails:** Check your internet connection and disk space, retry the automatic download, or use the manual model setup described above.
* **Application freezes or uses too many resources:**close and restart it or  Try Tiny or Base, close other resource-intensive applications, and.
- **Incorrect characters in an SRT file:** Convert the file to UTF-8 using the app's encoding tool or a text editor.
- **Translation fails:** Check your internet connection; translation uses an online service.
> 💡 **TIP: Non-English Language Accuracy**  
> The (Tiny, Base) models are extremely fast but perform best with English. For highly accurate and professional transcription of Arabic and other non-English           languages, it is highly recommended to use **Medium** or **Large** models.


---

*Developed by **RASHEED AL-RAJEHI @ SHADOW WOLF SECURITY***
