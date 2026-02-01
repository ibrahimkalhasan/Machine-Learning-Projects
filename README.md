# Voice Grammar Monitor

Voice Grammar Monitor is a Python project that turns live or recorded speech into real-time grammar feedback, keyword alerts, and a professional speaking report. It is designed for coaching, call-center QA, and speaker improvement.

## What it does

- **Speech-to-text** with streaming audio chunks or audio files.
- **Grammar mistake detection** with actionable feedback.
- **Real-time keyword detection** and alerting (console + webhook).
- **Professional speaking report** summarizing filler words, grammar errors, and clarity signals.

## Architecture overview

```
Audio stream/file -> Transcriber -> Grammar Analyzer -> Keyword Detector -> Alerts
                                                        -> Report Generator
```

## Setup

1. Create a Python 3.10+ environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick start (file processing)

```bash
python main.py --audio-path data/sample.wav \
  --keywords "deadline,pricing,discount" \
  --webhook-url "https://example.com/alert"
```

## Quick start (live microphone)

```bash
python main.py --live --keywords "refund,escalate" --webhook-url "https://example.com/alert"
```

## Outputs

- Live console alerts when keywords appear.
- JSON + Markdown report saved to `reports/`.

## Configuration

You can customize thresholds, alert channels, and report options in `app/config.py`.

## Notes

- The project uses `faster-whisper` for transcription and `language-tool-python` for grammar analysis.
- For best real-time performance, run on a GPU and set `compute_type="float16"` in `app/transcribe.py`.

## Roadmap

- Add diarization (speaker separation).
- Extend professional speaking score with more prosody signals.
- Add email + Slack alert integrations.
