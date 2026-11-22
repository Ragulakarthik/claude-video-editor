"""Local Whisper transcriber that writes Scribe-shaped JSON (video-use compatible).

Usage:
    python helpers_local/transcribe_whisper.py <video> --edit-dir <edit_dir> [--model medium] [--language te]
Output: <edit_dir>/transcripts/<video_stem>.json  ({"words":[{type,text,start,end,speaker_id}]})
Nothing is uploaded; audio never leaves this machine.
"""
import argparse, json, sys
from pathlib import Path
from faster_whisper import WhisperModel

ap = argparse.ArgumentParser()
ap.add_argument("video", type=Path)
ap.add_argument("--edit-dir", type=Path, required=True)
ap.add_argument("--model", default="medium")
ap.add_argument("--language", default=None, help="e.g. te, en; omit to auto-detect")
ap.add_argument("--no-vad", action="store_true", help="disable voice-activity filter (keeps quiet/mixed speech)")
a = ap.parse_args()

out = a.edit_dir / "transcripts" / f"{a.video.stem}.json"
if out.exists():
    print(f"cached: {out.name}"); sys.exit(0)
out.parent.mkdir(parents=True, exist_ok=True)

model = WhisperModel(a.model, device="cpu", compute_type="int8")
segs, info = model.transcribe(str(a.video), language=a.language, word_timestamps=True,
                              vad_filter=not a.no_vad, beam_size=5)
words, prev_end = [], None
for s in segs:
    for w in s.words or []:
        if prev_end is not None and w.start > prev_end:
            words.append({"type": "spacing", "text": " ", "start": prev_end, "end": w.start})
        words.append({"type": "word", "text": w.word.strip(), "start": w.start,
                      "end": w.end, "speaker_id": "speaker_0"})
        prev_end = w.end
out.write_text(json.dumps({"language_code": info.language, "words": words}, ensure_ascii=False))
print(f"wrote {out} ({sum(x['type']=='word' for x in words)} words, lang={info.language})")
