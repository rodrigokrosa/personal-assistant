import sys

from ollama import Client

sys.path.append("/home/isi/code/personal-assistant")
from utils.audio import generate_streaming_audio


def add_two_numbers(a: int, b: int) -> int:
    """Soma dois numeros inteiros.

    Args:
      a (int): O primeiro numero inteiro
      b (int): O segundo numero inteiro

    Returns:
      int: A soma dos dois numeros inteiros
    """
    return int(a) + int(b)


def control_lights(turn_on: bool) -> str:
    """Função para controlar as luzes, ligando ou desligando.

    Args:
      turn_on (bool): Se True, liga as luzes. Se False, desliga as luzes.

    Returns:
      str: Mensagem indicando se as luzes foram ligadas ou desligadas.
    """
    if turn_on:
        return "The lights are now on."
    else:
        return "The lights are now off."


available_tools = {"add_two_numbers": add_two_numbers, "control_lights": control_lights}


system_tool_message = """
    You have at your disposal tools to control lights and to sum integer numbers.
    Use them whenever needed by the user.
    When using tools, always check the variable types.
"""

system_message = (
    "You should always give reasonably short answers. Always respond in Brazilian Portuguese."
)


def tool_chat_tts(text: str):
    """Generate a response from the LLM model."""
    client = Client(
        # host="http://192.168.15.8:11434",
        host="http://127.0.0.1:11434"
    )

    messages = []

    messages.append({"role": "system", "content": system_tool_message})
    messages.append({"role": "user", "content": text})

    response = client.chat(
        # model="llama3.2:1b-instruct-q4_K_M",
        model="llama3.2:3b-tool",
        messages=messages,
        stream=False,
        tools=[add_two_numbers, control_lights],
    )

    punctuations = [".", "!", "?", ":", ";"]

    messages.append(response["message"])

    if response.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in response.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_tools.get(tool.function.name):
                print("<Calling function:", tool.function.name, ">")
                print("<Arguments:", tool.function.arguments, ">")
                output = function_to_call(**tool.function.arguments)
                print("<Function output:", output, ">")
            else:
                print("Function", tool.function.name, "not found")

        # Add the function response to messages for the model to use
        messages.append(response.message)
        messages.append({"role": "tool", "content": str(output), "name": tool.function.name})

        messages.append(
            {
                "role": "user",
                "content": "Give an answer using the tool output as an action taken by you."
                + "Always respond in Brazilian Portuguese.",
            }
        )

        # Get final response from model with function outputs
        final_response = client.chat(model="llama3.2:3b", messages=messages)
        llm_response = final_response["message"]["content"]
    else:
        print("<No tool calls returned from model>")
        final_response = client.chat(
            # host="http://192.168.15.8:11434",
            host="http://127.0.0.1:11434",
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text},
            ],
        )
        llm_response = final_response["message"]["content"]

    llm_response = llm_response.replace("*", "")

    current_group = ""
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
            tool_chat_tts(input_text)
        except KeyboardInterrupt:
            print("\n\nSaindo do programa...")
            break
