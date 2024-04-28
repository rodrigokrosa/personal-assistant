import sys

import ollama

sys.path.append("/home/koba/code/personal-assistant")
from utils.audio import generate_streaming_audio


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
                print(f"\033[36m{current_group}\033[0m", end="", flush=True)
                generate_streaming_audio(current_group)
            current_group = ""
    if current_group.strip():
        groups.append(current_group)
        print(f"\033[36m{current_group}\033[0m")
        generate_streaming_audio(current_group)
    return groups


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
            print("\033[92mLLM\033[0m: ", end="")
            streaming_chat_tts(input_text)
        except KeyboardInterrupt:
            print("\n\nSaindo do programa...")
            break
