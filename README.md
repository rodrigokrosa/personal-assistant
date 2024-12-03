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

```
git clone https://github.com/rhasspy/piper.git
```

2. Go to python_run folder

```
cd piper/src/python_run
```

3. Install piper-tts

```
pip install -e .
```

4. Install requirements for the http_server

```
pip install -r requirements_http.txt
```

5. Download onxx pretrained models from the repository [\[link\]](https://github.com/rhasspy/piper/blob/master/VOICES.md)

6. Run http_server with at the folder with the model downloaded:

```
screen python -m piper.http_server --model <model_name>
```

# LLM HTTP Server with Ollama

1. Install ollama

```
curl -fsSL https://ollama.com/install.sh | sh
```

2. Init ollama server

```
screen -S llm ollama serve
```

3. Test and download llm model

```
ollama run llama3
```

# Raspberry pi config:

```
curl https://pyenv.run | bash
```

```
curl -sSL https://install.python-poetry.org | python3 -
```

```
nano ~/.bashrc
```

```
# Pyenv setup
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

```
export PATH="$HOME/.local/bin:$PATH"
```

```
source ~/.bashrc
```
