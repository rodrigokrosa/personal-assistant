#! /bin/bash

screen -S tts python -m piper.http_server --model pt_BR-faber-medium.onnx
