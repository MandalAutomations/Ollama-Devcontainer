import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import requests
import json

SAMPLE_RATE = 16000
MODEL_NAME = "whisper"  # or whisper-small, whisper-medium, whisper-large

def record_audio(duration=5):
    print("🎤 Recording... Speak now.")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()

    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_wav.name, SAMPLE_RATE, audio)

    return temp_wav.name

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
    audio_file = record_audio(5)  # record 5 seconds
    transcribe_ollama(audio_file)
