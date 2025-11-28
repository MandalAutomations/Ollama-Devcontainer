import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import requests
import json
import os
from datetime import datetime

SAMPLE_RATE = 16000
MODEL_NAME = "whisper"  # or whisper-small, whisper-medium, whisper-large

def record_audio(duration=5, output_folder=None):
    print("🎤 Recording... Speak now.")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()

    timestamp = datetime.now().strftime("%Y%m%_%H%M%S")
    filename = f"{timestamp}.wav"
    
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        audio_path = os.path.join(output_folder, filename)
    else:
        audio_path = filename
    
    print(f"💾 Audio recorded to {audio_path}")
    write(audio_path, SAMPLE_RATE, audio)

    return audio_path

def transcribe_ollama(audio_path):
    print("🔁 Sending audio to Ollama Whisper…")

    with open(audio_path, "rb") as f:
        files = {"file": f}
        data = {
            "model": MODEL_NAME,
            "options": {"temperature": 0}
        }

        response = requests.post(
            "http://localhost:11434/api/audio/transcriptions",
            data=data,
            files=files
        )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    result = response.json()
    print("\n📝 Transcription:")
    print(result["text"])
    return result["text"]

if __name__ == "__main__":
    # Example usage:
    # Save to current directory with timestamp
    # audio_file = record_audio(5)
    
    # Save to specific folder with timestamp
    output_folder = "recordings"  # Change this to your desired folder
    audio_file = record_audio(5, output_folder)  # record 5 seconds
    # transcribe_ollama(audio_file)
