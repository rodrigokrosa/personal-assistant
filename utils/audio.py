import io
import time

import requests
import sounddevice as sd
from scipy.io import wavfile


def generate_audio_wav(text: str, output_file: str):
    """Generate a WAV file from a text using the TTS API."""
    url = "http://localhost:5000"
    payload = {"text": text}
    result = requests.get(url, params=payload)  # nosec
    with open(output_file, "wb") as f:
        for chunk in result.iter_content(chunk_size=128):
            f.write(chunk)


def generate_audio_array(text: str):
    """Generate a WAV file from a text using the TTS API."""
    url = "http://localhost:5000"
    payload = {"text": text}
    result = requests.get(url, params=payload)  # nosec
    wav_io = io.BytesIO(result.content)
    rate, data = wavfile.read(wav_io)
    return rate, data


def generate_streaming_audio(text: str):
    """Generate a WAV file from a text using the TTS API."""
    rate, data = generate_audio_array(text)
    sd.play(data, rate)
    sd.wait()
    time.sleep(0.5)
