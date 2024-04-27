import ollama
import requests
import scipy.io.wavfile as wavfile
from IPython.display import Audio


def generate_llm_response(text: str):
    """Generate a response from the LLM model."""
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": text,
            },
        ],
    )
    return response["message"]["content"]


def generate_audio_wav(text: str, output_file: str):
    """Generate a WAV file from a text using the TTS API."""
    url = "http://localhost:5000"

    payload = {"text": text}

    result = requests.get(url, params=payload)  # nosec

    with open(output_file, "wb") as f:
        for chunk in result.iter_content(chunk_size=128):
            f.write(chunk)


def play_wav_file(file: str):
    """Play a WAV file and return the audio data and sample rate."""
    rate, data = wavfile.read(file)
    return data, rate


def chat_tts(input_text: str):
    """Chat with the LLM model and generate a TTS response."""
    llm_response = generate_llm_response(input_text)

    generate_audio_wav(llm_response, "../output/output.wav")

    data, rate = play_wav_file("../output/output.wav")

    return data, rate


data, rate = chat_tts("Oi, como vai você")
Audio(data, rate=rate)
