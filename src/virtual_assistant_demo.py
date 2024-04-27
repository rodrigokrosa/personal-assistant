import ollama
import requests
import scipy.io.wavfile as wavfile
import sounddevice as sd


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
    llm_response = response["message"]["content"]
    llm_response = llm_response.replace("*", "")
    print(f"\033[92mLLM\033[0m: \033[36m{llm_response}\033[0m")

    return llm_response


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


if __name__ == "__main__":
    while True:
        try:
            input_text = input("\033[34mUser\033[0m: ").strip()
            if not input_text:
                print("Input cannot be empty. Please try again.")
                continue
            if len(input_text) > 100:
                print("Input is too long. Please enter 100 characters or less.")
                continue
            data, rate = chat_tts(input_text)
            sd.play(data, rate)
        except KeyboardInterrupt:
            print("Exiting the program...")
            break
