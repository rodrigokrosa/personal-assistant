import collections
import time
import wave

import pyaudio
import webrtcvad


def record_audio(
    output_filename, sample_rate=16000, chunk_size=320, channels=1, silence_threshold=2
):
    """Record audio from the microphone until silence is detected."""
    audio = pyaudio.PyAudio()
    vad = webrtcvad.Vad()
    vad.set_mode(1)  # 0: Normal, 1: Low Bitrate, 2: Aggressive, 3: Very Aggressive

    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )
    print("\nListening for speech...")

    frames = []
    speech_frames = []
    silence_start = None
    ring_buffer = collections.deque(maxlen=int(silence_threshold * sample_rate / chunk_size))

    # Listen for speech to start recording
    while True:
        data = stream.read(chunk_size)
        if len(data) != chunk_size * 2:  # Ensure the frame size is correct
            continue
        is_speech = vad.is_speech(data, sample_rate)
        if is_speech:
            speech_frames.append(data)
            if len(speech_frames) * (chunk_size / sample_rate) > 0.5:
                frames.extend(speech_frames)
                break
        else:
            speech_frames.clear()

    print("Recording...")

    while True:
        data = stream.read(chunk_size)
        if len(data) != chunk_size * 2:  # Ensure the frame size is correct
            continue
        is_speech = vad.is_speech(data, sample_rate)
        ring_buffer.append((data, is_speech))

        if is_speech:
            frames.extend([frame for frame, speech in ring_buffer])
            ring_buffer.clear()
            silence_start = None
        else:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > silence_threshold:
                break

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(output_filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()


if __name__ == "__main__":
    record_audio("audio.wav", sample_rate=16000, silence_threshold=2)
