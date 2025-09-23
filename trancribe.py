import whisper

# Load a Whisper model: options are tiny, base, small, medium, large
model = whisper.load_model("base")

# Transcribe the audio file (supports wav, mp3, m4a, and more)
result = model.transcribe("NVIDIA CEO Jensen Huang's Vision for the Future.mp3")

# Print transcription text
print(result["text"])
