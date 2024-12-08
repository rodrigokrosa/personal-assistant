import sys

from ollama import Client

sys.path.append("/home/isi/code/personal-assistant")
from utils.audio import generate_streaming_audio


def streaming_chat_tts(text: str):
    """Generate a response from the LLM model."""
    client = Client(
        # host="http://192.168.15.8:11434"
        host="http://127.0.0.1:11434"
    )

    system_message = (
        "You should always give reasonably short answers. Always respond in Brazilian Portuguese."
    )

    stream = client.chat(
        # model="llama3.2:1b-instruct-q4_K_M",
        model="llama3.2:3b",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": text},
        ],
        stream=True,
    )

    punctuations = [".", "!", "?", ":", ";"]

    current_group = ""
    for chunk in stream:
        llm_response = chunk["message"]["content"]
        llm_response = llm_response.replace("*", "")

        # Process the chunk to split at punctuation marks
        while any(punct in llm_response for punct in punctuations):
            for punct in punctuations:
                if punct in llm_response:
                    part, llm_response = llm_response.split(punct, 1)
                    current_group += part + punct
                    if current_group.strip():
                        print(f"\033[36m{current_group}\033[0m", end="", flush=True)
                        generate_streaming_audio(current_group)
                    current_group = ""
                    break

        current_group += llm_response

    if current_group.strip():
        print(f"\033[36m{current_group}\033[0m")
        generate_streaming_audio(current_group)


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
