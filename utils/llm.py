import ollama
import sounddevice as sd

from .audio import generate_audio_array


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


def chat_tts(input_text: str):
    """Chat with the LLM model and generate a TTS response."""
    llm_response = generate_llm_response(input_text)
    rate, data = generate_audio_array(llm_response)
    sd.play(data, rate)
    sd.wait()
