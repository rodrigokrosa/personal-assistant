import time

import torch
from IPython.display import Audio
from transformers import AutoProcessor, BarkModel

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained(
    "suno/bark-small",
    torch_dtype=torch.float16,
)
model.enable_cpu_offload()
model = model.to_bettertransformer()

sample_rate = model.generation_config.sample_rate


def generate_audio(text: str, voice_preset: str = "v2/pt_speaker_8"):
    """Generate audio from text using the Bark model."""
    inputs = processor(
        text,
        voice_preset=voice_preset,
        return_tensors="pt",
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        audio_array = model.generate(**inputs)

    audio_array = audio_array.cpu().numpy().squeeze()

    return audio_array


start_time = time.time()
audio_array = generate_audio(
    text="Olá, sou seu assistente pessoal! Como posso ajudá-lo?",
    voice_preset="v2/pt_speaker_8",
)
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")

Audio(audio_array, rate=sample_rate)
