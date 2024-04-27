import requests

text = (
    "Bem vindo ao mundo da síntese de voz! Esse é um exemplo do sistema Piper de síntese de voz."
)
url = "http://localhost:5000"
output_file = "../output/pt-br-edresson-low.wav"

payload = {"text": text}

result = requests.get(url, params=payload)  # nosec

with open(output_file, "wb") as f:
    for chunk in result.iter_content(chunk_size=128):
        f.write(chunk)
