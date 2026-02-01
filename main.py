import argparse
import pathlib

from app.alerts import AlertDispatcher
from app.config import AppConfig
from app.grammar import GrammarAnalyzer
from app.keywords import KeywordDetector
from app.report import ReportBuilder
from app.stream import LiveAudioStream, file_audio_stream
from app.transcribe import Transcriber


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Voice grammar monitoring with alerts.")
    parser.add_argument("--audio-path", type=pathlib.Path, help="Path to audio file.")
    parser.add_argument("--live", action="store_true", help="Use live microphone input.")
    parser.add_argument("--keywords", type=str, default="", help="Comma-separated keywords.")
    parser.add_argument("--webhook-url", type=str, default="", help="Webhook URL for alerts.")
    parser.add_argument("--report-dir", type=pathlib.Path, default=pathlib.Path("reports"))
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if not args.live and not args.audio_path:
        raise SystemExit("Provide --audio-path or --live for microphone input.")

    config = AppConfig.from_cli(args)

    transcriber = Transcriber(config.transcription)
    grammar = GrammarAnalyzer(config.grammar)
    keywords = KeywordDetector(config.keywords)
    alerts = AlertDispatcher(config.alerts)
    report = ReportBuilder(config.report)

    if args.live:
        stream = LiveAudioStream(config.audio)
    else:
        stream = file_audio_stream(args.audio_path, config.audio)

    for chunk in stream:
        transcript = transcriber.transcribe_chunk(chunk)
        if not transcript:
            continue

        grammar_result = grammar.analyze(transcript)
        keyword_hits = keywords.detect(transcript)

        if keyword_hits:
            alerts.send_keyword_alert(keyword_hits, transcript)

        report.update(transcript, grammar_result, keyword_hits)

    report_path = report.finalize()
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
