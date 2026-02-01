from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
from faster_whisper import WhisperModel

from app.config import TranscriptionConfig


@dataclass
class TranscriptionChunk:
    audio: np.ndarray
    sample_rate: int


class Transcriber:
    def __init__(self, config: TranscriptionConfig) -> None:
        self.config = config
        self.model = WhisperModel(
            config.model_size,
            compute_type=config.compute_type,
        )

    def transcribe_chunk(self, chunk: TranscriptionChunk) -> str:
        if chunk.audio.size == 0:
            return ""
        segments, _info = self.model.transcribe(
            chunk.audio,
            language=self.config.language,
            vad_filter=True,
        )
        text_parts = [segment.text.strip() for segment in segments if segment.text.strip()]
        return " ".join(text_parts)
