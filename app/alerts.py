from __future__ import annotations

from dataclasses import dataclass

import requests
from rich.console import Console

from app.config import AlertConfig
from app.keywords import KeywordHit


@dataclass
class AlertDispatcher:
    config: AlertConfig

    def __post_init__(self) -> None:
        self.console = Console()

    def send_keyword_alert(self, hits: tuple[KeywordHit, ...], transcript: str) -> None:
        keywords = ", ".join(f"{hit.keyword}({hit.count})" for hit in hits)
        message = f"Keyword alert: {keywords}\nTranscript: {transcript}"
        self.console.print(f"[bold yellow]{message}[/bold yellow]")

        if not self.config.webhook_url:
            return

        payload = {
            "type": "keyword_alert",
            "keywords": [hit.keyword for hit in hits],
            "counts": {hit.keyword: hit.count for hit in hits},
            "transcript": transcript,
        }
        requests.post(self.config.webhook_url, json=payload, timeout=5)
