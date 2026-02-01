from __future__ import annotations

from dataclasses import dataclass

from app.config import KeywordConfig


@dataclass
class KeywordHit:
    keyword: str
    count: int


class KeywordDetector:
    def __init__(self, config: KeywordConfig) -> None:
        self.keywords = tuple(keyword.lower() for keyword in config.keywords)

    def detect(self, transcript: str) -> tuple[KeywordHit, ...]:
        transcript_lower = transcript.lower()
        hits: list[KeywordHit] = []
        for keyword in self.keywords:
            if not keyword:
                continue
            count = transcript_lower.count(keyword)
            if count:
                hits.append(KeywordHit(keyword=keyword, count=count))
        return tuple(hits)
