# Steps when initiating a new ML python project

1. Create folder structure

2. Configure pyenv

```bash
pyenv local 3.10
```

3. Initialize poetry

```bash
poetry init
```

4. Initialize pre-commit

```bash
pre-commit install
```

# TTS HTTP Server with Piper TTS

1. Clone Piper-TTS repository

```bash
git clone https://github.com/rhasspy/piper.git
```

2. Go to python_run folder

```bash
cd piper/src/python_run
```

3. Install piper-tts

```bash
pip install -e .
```

4. Install requirements for the http_server

```bash
pip install -r requirements_http.txt
```

5. Download onxx pretrained models from the repository [\[link\]](https://github.com/rhasspy/piper/blob/master/VOICES.md)

6. Run http_server with at the folder with the model downloaded:

```bash
screen python -m piper.http_server --model <model_name>
```

# LLM HTTP Server with Ollama

1. Install ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Init ollama server

```bash
ollama serve
```

3. Test and download llm model

```bash
ollama run llama3.2:3b
```

4. Get llama modelfile

```bash
ollama show llama3.2:3b --modelfile > Modelfile3.2
```

5. Modify llama modelfile tool prompt

```
...

{{ range $.Tools }}
{{- . }}
{{ end }}
Question: {{ .Content }}<|eot_id|>
{{- else }}

Analyse the given prompt and decide whether or not it can be answered by a tool.  If it can, use the following functions to respond with a JSON for a function call with its proper arguments that best answers the given prompt.  Respond in the format {"name": function name, "parameters": dictionary of argument name and its value}. Do not use variables.

{{ .Content }}<|eot_id|>
{{- end }}{{ if $last }}<|start_header_id|>assistant<|end_header_id|>

...
```

6. Create a new model using this modified modelfile

```bash
ollama create llama3.2:3b-tool -f Modelfile3.2
```

# Raspberry pi config:

1. Install Pyenv to manage python versions

```bash
curl https://pyenv.run | bash
```

2. Install poetry to manage libraries

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Modify PATH for pyenv and poetry

```bash
nano ~/.bashrc
```

```bash
# Pyenv setup
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

```bash
export PATH="$HOME/.local/bin:$PATH"
```

```bash
source ~/.bashrc
```

4. Install linux audio library needed

```bash
sudo apt install portaudio19-dev
```

5. Start poetry and install libs

```bash
poetry shell
poetry install
```

6. If using Raspberry Pi GPIO pins, install RPi.GPIO

```bash
poetry add RPi.GPIO
```

7. Go to the file and modify OLLAMA HOST if using API from another computer

```python
client = Client(
    # host="http://192.168.15.8:11434",
    host="http://127.0.0.1:11434"
)
```
