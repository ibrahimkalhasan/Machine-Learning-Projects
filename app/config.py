from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class AudioConfig:
    sample_rate: int = 16000
    block_seconds: float = 4.0


@dataclass(frozen=True)
class TranscriptionConfig:
    model_size: str = "small"
    compute_type: str = "int8"
    language: str = "en"


@dataclass(frozen=True)
class GrammarConfig:
    language: str = "en-US"


@dataclass(frozen=True)
class KeywordConfig:
    keywords: tuple[str, ...]


@dataclass(frozen=True)
class AlertConfig:
    webhook_url: str = ""


@dataclass(frozen=True)
class ReportConfig:
    output_dir: str = "reports"


@dataclass(frozen=True)
class AppConfig:
    audio: AudioConfig
    transcription: TranscriptionConfig
    grammar: GrammarConfig
    keywords: KeywordConfig
    alerts: AlertConfig
    report: ReportConfig

    @staticmethod
    def parse_keywords(value: str) -> tuple[str, ...]:
        if not value:
            return ()
        cleaned = [item.strip() for item in value.split(",") if item.strip()]
        return tuple(cleaned)

    @classmethod
    def from_cli(cls, args: object) -> "AppConfig":
        keywords = cls.parse_keywords(getattr(args, "keywords", ""))
        return cls(
            audio=AudioConfig(),
            transcription=TranscriptionConfig(),
            grammar=GrammarConfig(),
            keywords=KeywordConfig(keywords=keywords),
            alerts=AlertConfig(webhook_url=getattr(args, "webhook_url", "")),
            report=ReportConfig(output_dir=str(getattr(args, "report_dir", "reports"))),
        )


def format_keywords(keywords: Iterable[str]) -> str:
    return ", ".join(keywords) if keywords else "none"
