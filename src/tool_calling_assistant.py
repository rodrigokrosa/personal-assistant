import sys

# import RPi.GPIO as GPIO
from faster_whisper import WhisperModel
from ollama import Client

# sys.path.append("/home/personal/personal-assistant")
sys.path.append("/home/isi/code/personal-assistant")

from detect_speech_silence import record_audio
from utils.audio import generate_streaming_audio


def add_two_numbers(a: int, b: int) -> int:
    """Sum two integer numbers.

    Args:
      a (int): The first integer number
      b (int): The second integer number

    Returns:
      int: Sum of two integer numbers
    """
    return int(a) + int(b)


def control_lights(turn_on: bool) -> str:
    """Function to control the lights, turning them on and off.

    Args:
      turn_on (bool): If True, turn on the lights. If False, turn off the lights.

    Returns:
      str: Message indicating if the lights were turned on or off.
    """
    if isinstance(turn_on, str):
        if turn_on.lower().strip() == "true":
            turn_on = True
        elif turn_on.lower().strip() == "false":
            turn_on = False
        else:
            return "Invalid argument"
    if turn_on:
        # GPIO.output(LED_PIN, GPIO.HIGH)
        return "The lights are now on."
    else:
        # GPIO.output(LED_PIN, GPIO.LOW)
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
        # host="http://192.168.15.6:11434",
        host="http://127.0.0.1:11434"
    )

    messages = []

    messages.append({"role": "system", "content": system_tool_message})
    messages.append({"role": "user", "content": text})

    response = client.chat(
        # model="llama3.2:1b-instruct-q4_K_M",
        model="llama3.1:8b-tool",
        # model="llama3.2:3b-tool",
        messages=messages,
        stream=False,
        tools=[add_two_numbers, control_lights],
    )

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
        messages.append({"role": "tool", "content": str(output), "name": tool.function.name})

        messages.append(
            {
                "role": "user",
                "content": "Give an answer using the tool output as an action taken by you."
                + "Always respond in Brazilian Portuguese.",
            }
        )

        # Get final response from model with function outputs
        final_response = client.chat(model="llama3.1", messages=messages)
        llm_response = final_response["message"]["content"]
    else:
        print("<No tool calls returned from model>")
        final_response = client.chat(
            model="llama3.1",
            # model="llama3.2:3b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": text},
            ],
        )
        llm_response = final_response["message"]["content"]

    llm_response = llm_response.replace("*", "")

    punctuations = [".", "!", "?", ":", ";"]

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
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")

    # # Set up the GPIO pin numbering
    # GPIO.setmode(GPIO.BCM)

    # # Define the GPIO pin number where the LED is connected
    # LED_PIN = 18

    # # Set up the GPIO pin as an output
    # GPIO.setup(LED_PIN, GPIO.OUT)
    # GPIO.output(LED_PIN, GPIO.LOW)

    while True:
        try:
            record_audio("output/audio.wav", sample_rate=16000, silence_threshold=1.5)

            segments, info = model.transcribe(
                "output/audio.wav",
                beam_size=5,
                vad_filter=True,  # , language="pt"
            )

            input_text = [segment.text for segment in segments]
            if not input_text:
                print("Nenhuma entrada detectada. Por favor, tente novamente.")
                continue
            else:
                input_text = "".join(input_text).strip()
                print("\n\033[34mUser\033[0m: ", input_text)

            # input_text = input("\n\033[34mUser\033[0m: ").strip()
            # if not input_text:
            #     print("Entrada não pode ser vazia. Por favor, tente novamente.")
            #     continue

            # LLM Response
            print("\033[92mLLM\033[0m: ", end="")
            tool_chat_tts(input_text)

        except KeyboardInterrupt:
            # Clean up GPIO settings when the script exits
            # import atexit

            # atexit.register(GPIO.cleanup)
            print("\n\nSaindo do programa...")
            break
