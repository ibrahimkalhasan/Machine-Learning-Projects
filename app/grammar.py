from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import language_tool_python

from app.config import GrammarConfig


@dataclass
class GrammarIssue:
    message: str
    rule_id: str
    offset: int
    length: int
    context: str
    replacements: tuple[str, ...]


@dataclass
class GrammarResult:
    issues: tuple[GrammarIssue, ...]

    @property
    def error_count(self) -> int:
        return len(self.issues)


class GrammarAnalyzer:
    def __init__(self, config: GrammarConfig) -> None:
        self.tool = language_tool_python.LanguageTool(config.language)

    def analyze(self, text: str) -> GrammarResult:
        matches = self.tool.check(text)
        issues: list[GrammarIssue] = []
        for match in matches:
            issues.append(
                GrammarIssue(
                    message=match.message,
                    rule_id=match.ruleId,
                    offset=match.offset,
                    length=match.errorLength,
                    context=match.context,
                    replacements=tuple(match.replacements),
                )
            )
        return GrammarResult(tuple(issues))
