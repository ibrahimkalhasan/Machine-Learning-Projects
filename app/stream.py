from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np
import sounddevice as sd

from app.config import AudioConfig
from app.transcribe import TranscriptionChunk


@dataclass
class LiveAudioStream:
    config: AudioConfig

    def __iter__(self) -> Iterator[TranscriptionChunk]:
        block_size = int(self.config.sample_rate * self.config.block_seconds)
        with sd.InputStream(channels=1, samplerate=self.config.sample_rate) as stream:
            while True:
                audio, _overflowed = stream.read(block_size)
                audio = np.squeeze(audio).astype(np.float32)
                yield TranscriptionChunk(audio=audio, sample_rate=self.config.sample_rate)


def file_audio_stream(path: str, config: AudioConfig) -> Iterator[TranscriptionChunk]:
    import soundfile as sf

    audio, sample_rate = sf.read(path)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    chunk_size = int(sample_rate * config.block_seconds)
    for start in range(0, len(audio), chunk_size):
        chunk = audio[start : start + chunk_size].astype(np.float32)
        yield TranscriptionChunk(audio=chunk, sample_rate=sample_rate)
