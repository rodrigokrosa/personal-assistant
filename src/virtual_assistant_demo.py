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


def chat_tts(input_text: str):
    """Chat with the LLM model and generate a TTS response."""
    llm_response = generate_llm_response(input_text)
    generate_audio_wav(llm_response, "../output/output.wav")
    rate, data = wavfile.read("../output/output.wav")
    sd.play(data, rate)
    sd.wait()


def streaming_chat_tts(text: str):
    """Generate a response from the LLM model."""
    stream = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": text}],
        stream=True,
    )
    groups = []
    current_group = ""
    for chunk in stream:
        llm_response = chunk["message"]["content"]
        llm_response = llm_response.replace("*", "")
        current_group += llm_response
        if llm_response.endswith((".", "!", "?")):
            if current_group.strip():
                groups.append(current_group)
                print(current_group, end="", flush=True)
                generate_streaming_audio(current_group)
            current_group = ""
    if current_group.strip():
        groups.append(current_group)
        print(current_group)
        generate_streaming_audio(current_group)
    return groups


def generate_streaming_audio(text: str):
    """Generate a WAV file from a text using the TTS API."""
    generate_audio_wav(text, "../output/output.wav")
    rate, data = wavfile.read("../output/output.wav")
    sd.play(data, rate)
    sd.wait()


if __name__ == "__main__":
    print("Bem vindo ao demo do assistente virtual!")
    while True:
        try:
            input_text = input("\n\033[34mUser\033[0m: ").strip()
            if not input_text:
                print("Entrada não pode ser vazia. Por favor, tente novamente.")
                continue
            if len(input_text) > 100:
                print("Entrada muito longa. Por favor, entre com menos de 100 caracteres.")
                continue
            streaming_chat_tts(input_text)
        except KeyboardInterrupt:
            print("\n\nSaindo do programa...")
            break
