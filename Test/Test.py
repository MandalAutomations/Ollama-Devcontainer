import whisper

# Load a Whisper model (e.g., 'base', 'small', 'medium', 'large')
# The first time you use a model, it will be downloaded.
model = whisper.load_model("base")

# Transcribe an audio file
result = model.transcribe("your_audio_file.mp3")

# Print the transcribed text
print(result["text"])
