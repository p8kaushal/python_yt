# python_yt

An automated end-to-end Python pipeline designed to scrape YouTube videos, extract high-quality audio streams, generate speech-to-text transcriptions with OpenAI Whisper, produce summaries using local LLMs via Ollama, and persist structured metadata with Prisma ORM.

---

## Features

- **Multi-Source Scraping**: Extract videos via YouTube Channel ID, Playlist ID, search keywords, or direct video URLs without hitting YouTube Data API quota restrictions (via `scrapetube`).
- **Audio Extraction**: Download and convert video audio to optimized MP3 streams using `yt-dlp` and `FFmpeg`.
- **Speech-to-Text Transcription**: Transcribe video audio locally using OpenAI's `whisper` models (`base`, `tiny`, `small`, `medium`, `large`).
- **AI Summarization**: Generate concise video summaries using local LLM inference with Ollama (defaulting to Google's `gemma2:2b`).
- **Database Persistence**: Store content groups, video metadata, URLs, and summaries in a relational database (PostgreSQL / Supabase or SQLite) using `prisma-client-py`.

---

## Tech Stack

- **Language**: Python 3.10+
- **Ingestion & Scraping**: [`yt-dlp`](https://github.com/yt-dlp/yt-dlp), [`scrapetube`](https://github.com/dermasmid/scrapetube)
- **Audio Processing**: [FFmpeg](https://ffmpeg.org/)
- **Transcription**: [`openai-whisper`](https://github.com/openai/whisper), [PyTorch](https://pytorch.org/)
- **LLM Summarization**: [Ollama](https://ollama.com/) (e.g., `gemma2:2b`)
- **Database & ORM**: [Prisma Python Client](https://prisma-client-py.readthedocs.io/) (`prisma`), PostgreSQL / Supabase, SQLite
- **Configuration & Utilities**: `python-dotenv`, `requests`, `asyncio`

---

## Prerequisites

1. **Python 3.10+**
2. **FFmpeg**: Required for audio conversion.
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt update && sudo apt install ffmpeg`
   - **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or install via `winget install Gyan.FFmpeg`
3. **Ollama**: For local AI summaries.
   - Download and install from [ollama.com](https://ollama.com/)
   - Pull the default summarization model:
     ```bash
     ollama pull gemma2:2b
     ```

---

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/p8kaushal/python_yt.git
cd python_yt
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install yt-dlp scrapetube openai-whisper prisma python-dotenv requests torch
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DATABASE_URL="postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>?pgbouncer=true"
DIRECT_URL="postgresql://<USER>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"
```
*(Note: If using SQLite, adjust `schema.prisma` to use `provider = "sqlite"` and `url = "file:database.db"`).*

### 5. Setup Prisma ORM
Push the database schema and generate the Python Prisma client:
```bash
prisma db push
prisma py generate
```

---

## Usage

### Main Processing Pipeline (`get_vid_url.py`)
Run the unified ingestion, transcription, and summarization pipeline:

- **By Channel ID**:
  ```bash
  python get_vid_url.py -c channel -v UCedIWVVm-tkgAoZYQiT7Fvw
  ```
- **By Playlist ID**:
  ```bash
  python get_vid_url.py -c playlist -v PL1234567890abcdef
  ```
- **By Search Query**:
  ```bash
  python get_vid_url.py -c search -v "machine learning tutorial"
  ```
- **By Direct Video URL**:
  ```bash
  python get_vid_url.py -c direct -v "https://www.youtube.com/watch?v=7ARBJQn6QkM"
  ```
- **Custom Ollama Model**:
  ```bash
  python get_vid_url.py -c direct -v "https://www.youtube.com/watch?v=7ARBJQn6QkM" -m "llama3.2"
  ```

### Standalone Utilities
- **Audio Extraction**:
  ```bash
  python audio_extract.py
  ```
- **Audio Transcription**:
  ```bash
  python trancribe.py
  ```
- **Text Summarization**:
  ```bash
  python summarise.py
  ```
- **Whisper Sample Script**:
  ```bash
  python sample.py
  ```

---

## Project Structure

```text
python_yt/
├── app.py               # Basic yt-dlp video downloader
├── audio_extract.py     # Audio extraction script via yt-dlp & FFmpeg
├── dbtest.py            # Prisma database connection test
├── get_vid_url.py       # Main pipeline CLI (scraping, audio, whisper, ollama, prisma)
├── sample.py            # Standalone OpenAI Whisper transcription utility
├── summarise.py         # Ollama REST API text summarization script
├── trancribe.py         # Whisper transcription script
├── schema.prisma        # Prisma database schema definition
├── schema_test.prisma   # Test Prisma database schema
├── .gitignore           # Git ignore configuration
├── LICENSE              # MIT License
└── README.md            # Project documentation
```

---

## License

This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.
