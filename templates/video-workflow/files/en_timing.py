"""English-mode Whisper pass for TIMING ONLY (large-v3, local). Writes edit/transcripts/timing_en.json (absolute seconds).
Telugu speech comes out as English with clean word times, so scenes and captions can be synced to the spoken words."""
import json, os, sys
from faster_whisper import WhisperModel
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import glob, subprocess
SRC = sorted(glob.glob("../aroll/*.mp4"))[0]
OUT = "transcripts/timing_en.json"
DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))
WIN = [(a, min(a + 60, DUR)) for a in range(0, int(DUR) + 1, 60) if a < DUR]  # 60 s slices, whole video
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
allw = {}
for a, b in WIN:
    segs, _ = m.transcribe(SRC, language="en", word_timestamps=True, vad_filter=False, beam_size=5,
                           condition_on_previous_text=False, clip_timestamps=[a - 2 if a > 0 else 0, b + 2])
    for s in segs:
        for w in s.words or []:
            allw[(round(w.start, 2), w.word.strip())] = {"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)}
    out = sorted(allw.values(), key=lambda x: x["s"])
    json.dump(out, open(OUT, "w"))
    print(f"window {a}-{b} done, total words {len(out)}", flush=True)
print("ALL DONE", flush=True)
