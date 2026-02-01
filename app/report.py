from __future__ import annotations

from dataclasses import dataclass, field
import json
import pathlib
from typing import Iterable

from app.config import ReportConfig, format_keywords
from app.grammar import GrammarResult
from app.keywords import KeywordHit


@dataclass
class ReportBuilder:
    config: ReportConfig
    transcript: list[str] = field(default_factory=list)
    grammar_errors: list[dict] = field(default_factory=list)
    keyword_hits: dict[str, int] = field(default_factory=dict)

    def update(
        self,
        text: str,
        grammar: GrammarResult,
        hits: tuple[KeywordHit, ...],
    ) -> None:
        self.transcript.append(text)
        for issue in grammar.issues:
            self.grammar_errors.append(
                {
                    "message": issue.message,
                    "rule_id": issue.rule_id,
                    "context": issue.context,
                    "offset": issue.offset,
                    "length": issue.length,
                    "replacements": issue.replacements,
                }
            )
        for hit in hits:
            self.keyword_hits[hit.keyword] = self.keyword_hits.get(hit.keyword, 0) + hit.count

    def finalize(self) -> pathlib.Path:
        output_dir = pathlib.Path(self.config.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        report_data = {
            "summary": {
                "total_segments": len(self.transcript),
                "total_grammar_errors": len(self.grammar_errors),
                "keywords_detected": self.keyword_hits,
            },
            "transcript": self.transcript,
            "grammar_errors": self.grammar_errors,
        }
        json_path = output_dir / "report.json"
        json_path.write_text(json.dumps(report_data, indent=2), encoding="utf-8")

        markdown_path = output_dir / "report.md"
        markdown_path.write_text(self._to_markdown(report_data), encoding="utf-8")
        return markdown_path

    def _to_markdown(self, report_data: dict) -> str:
        summary = report_data["summary"]
        lines = [
            "# Professional Speaking Report",
            "",
            f"- Segments processed: {summary['total_segments']}",
            f"- Grammar errors detected: {summary['total_grammar_errors']}",
            f"- Keywords detected: {summary['keywords_detected'] or 'none'}",
            "",
            "## Transcript",
        ]
        for entry in self.transcript:
            lines.append(f"- {entry}")
        lines.append("")
        lines.append("## Grammar Issues")
        for error in self.grammar_errors:
            lines.append(f"- {error['message']} ({error['rule_id']})")
            lines.append(f"  - Context: {error['context']}")
            if error["replacements"]:
                replacements = ", ".join(error["replacements"])
                lines.append(f"  - Suggestions: {replacements}")
        return "\n".join(lines)
