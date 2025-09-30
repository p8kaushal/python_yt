# Installation requirement:
# pip install -U openai-whisper
# You may also need to install ffmpeg for proper audio handling:
# sudo apt update && sudo apt install ffmpeg (on Linux)
# brew install ffmpeg (on macOS)

import whisper
import os

# --- Configuration ---
# 1. Choose the model size. Options: 'tiny', 'base', 'small', 'medium', 'large'.
# 'tiny' is the fastest and smallest; 'large' is the slowest but most accurate.
MODEL_NAME = "base"

# 2. IMPORTANT: Replace this with the path to your actual audio file.
# Whisper supports various formats (MP3, WAV, FLAC, M4A, etc.)
AUDIO_FILE_PATH = "Ig0z0FE3gf0.mp3"
# ---------------------

def transcribe_audio(audio_path: str, model_name: str):
    """
    Loads a Whisper model and transcribes an audio file.
    """
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found at '{audio_path}'.")
        print("Please update the AUDIO_FILE_PATH variable to a valid file.")
        return

    try:
        # Load the specified model
        print(f"Loading Whisper model '{model_name}'...")
        model = whisper.load_model(model_name)

        # Perform the transcription
        print(f"Starting transcription for: {os.path.basename(audio_path)}...")
        
        # You can specify the language if known to improve accuracy:
        # result = model.transcribe(audio_path, language="en")
        
        result = model.transcribe(audio_path, fp16=False)

        # Print the full result text
        print("\n--- Full Transcription Result ---")
        print(result["text"].strip())
        print("---------------------------------")
        
        # Print detailed segment information (optional)
        print("\n--- Segment Details (Timestamped) ---")
        for segment in result["segments"]:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text'].strip()
            print(f"[{start_time:.2f}s - {end_time:.2f}s]: {text}")
        print("-------------------------------------")

    except Exception as e:
        print(f"\nAn error occurred during transcription: {e}")
        print("Ensure you have PyTorch, the Whisper package, and FFmpeg installed correctly.")


if __name__ == "__main__":
    transcribe_audio(AUDIO_FILE_PATH, MODEL_NAME)
