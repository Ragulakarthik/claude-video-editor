"""Compose preview: source video (never modified) + 11 scene clips + original sfx + Tenglish word captions.
Run from this folder:  python3 compose.py            -> preview_v1.mp4 (1080p preview)
No part of the video is cut. Original audio is kept untouched; sfx are mixed in quietly.
"""
import json, re, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
import glob
SRC = sorted(glob.glob("../aroll/*.mp4"))[0]  # the speaker footage (read-only copy of the original)
RES4K = os.environ.get("RES") == "4k"
W, H = (3840, 2160) if RES4K else (1920, 1080)
SCENES = "animations/scenes_4k.mp4" if RES4K else "animations/scenes.mp4"
OFF = json.load(open("animations/slot_scenes/offsets.json"))
DUR_TOTAL = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", SRC]))

# protected parts of the user's own footage (channel intro animation, end screen): never zoomed, graded, captioned or covered.
# edit/protected.json = [[start, end], ...]; "end" may be a large number to mean "to the end". Find them with find_protected.py.
PROT = [tuple(x) for x in json.load(open("protected.json"))] if os.path.exists("protected.json") else []
PROT = [(a, min(b, DUR_TOTAL + 1)) for a, b in PROT]
# scene start times, durations and sound-effect hits all come from animations/slot_scenes/scene_times.json (built by build_scenes.py)
ST = json.load(open("animations/slot_scenes/scene_times.json"))
T = {sid: v["T"] for sid, v in ST.items()}
FADE = 0.25

# ---- sound effect events: (type, source time) ----
ev = []
for sid, v in ST.items():
    ev.append(("whoosh", v["T"] - 0.05))
    ev.append(("swish", v["T"] + v["dur"] - 0.3))
    for r in v["pops"]:
        ev.append(("pop", v["T"] + r))
    for r in v["dings"]:
        ev.append(("ding", v["T"] + r))
ev.sort(key=lambda e: e[1])
VOL = {"whoosh": 0.35, "swish": 0.30, "pop": 0.45, "ding": 0.30}

# ---- sfx track ----
types = ["whoosh", "pop", "ding", "swish"]
inputs = []
for t in types:
    inputs += ["-i", f"sfx/{t}.wav"]
fc = []
labels = []
for ti, t in enumerate(types):
    n = sum(1 for e in ev if e[0] == t)
    outs = "".join(f"[{t}{k}]" for k in range(n))
    fc.append(f"[{ti}:a]asplit={n}{outs}" if n > 1 else f"[{ti}:a]anull[{t}0]")
    k = 0
    for e in ev:
        if e[0] != t:
            continue
        ms = int(max(0, e[1]) * 1000)
        fc.append(f"[{t}{k}]volume={VOL[t]},adelay={ms}|{ms}[d_{t}{k}]")
        labels.append(f"[d_{t}{k}]")
        k += 1
fc.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,apad=whole_dur={DUR_TOTAL:.3f},atrim=0:{DUR_TOTAL:.3f}[sfx]")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[sfx]", "-ar", "48000", "-ac", "2", "sfx_track.wav"], check=True)
print("sfx track ok, events:", len(ev))

# ---- English captions (from the approved English transcript; word by word, timing from Whisper phrase anchors) ----
try:  # optional Telugu-mode Whisper words (only used for the first rough spread; the English-mode timing overrides it)
    _f = sorted(glob.glob("transcripts/*.json"))
    _f = [f for f in _f if "timing" not in f]
    wh = json.load(open(_f[0]))
    W = [x for x in wh["words"] if x["type"] == "word" and x["end"] > x["start"]]
except Exception:
    W = []
segs = []
for line in open("transcripts/english_transcript.md", encoding="utf-8"):
    m = re.match(r"\[(\d+):(\d+)\]\s*(.+)", line.strip())
    if m:
        segs.append((int(m.group(1)) * 60 + int(m.group(2)), m.group(3)))
words = []  # (start, end, text)
seg_first = []  # (index of first word of each caption segment, segment start time)
for k, (t0, text) in enumerate(segs):
    t1 = segs[k + 1][0] if k + 1 < len(segs) else DUR_TOTAL
    toks = [x for x in text.split() if not (x.startswith('[') and x.endswith(']'))]
    if not toks:
        continue
    seg_first.append((len(words), float(t0)))
    ws = [w for w in W if t0 <= w["start"] < t1]
    L = [len(x) + 1 for x in toks]
    tot = sum(L)
    cum = [0]
    for l in L:
        cum.append(cum[-1] + l)
    if len(ws) >= max(4, 0.5 * len(toks)):
        n = len(ws)
        bt = [w["start"] for w in ws] + [ws[-1]["end"]]
        def mp(f):
            x = f * n
            i = min(int(x), n - 1)
            return bt[i] + (bt[i + 1] - bt[i]) * (x - i)
    else:
        a, b = t0 + 0.2, t1 - 0.3
        def mp(f, a=a, b=b):
            return a + (b - a) * f
    for j, tk in enumerate(toks):
        s = mp(cum[j] / tot)
        e = mp(cum[j + 1] / tot)
        s = min(max(s, t0), t1 - 0.15)          # stay inside this segment
        e = min(max(e, s + 0.12), t1, s + 1.4)  # never run into the next segment
        words.append([s, e, tk])


# ---- alignment anchors: match the approved English text to the words Whisper (English mode) heard ----
import difflib
A = []
if os.path.exists("transcripts/timing_en.json"):
    ew = [(re.sub(r"[^\w\-']", "", x["w"].lower()), x["s"]) for x in json.load(open("transcripts/timing_en.json"))]
    ew = [e for e in ew if e[0]]
    cw = [re.sub(r"[^\w\-']", "", w[2].lower()) for w in words]
    sm = difflib.SequenceMatcher(None, cw, [e[0] for e in ew], autojunk=False)
    for b in sm.get_matching_blocks():
        for k in range(b.size):
            if b.size >= 2 or len(cw[b.a + k]) >= 4:
                A.append((b.a + k, ew[b.b + k][1]))
    A.sort()
    keep = []
    for i, t in A:
        if keep and t <= keep[-1][1] + 0.02:
            continue
        keep.append((i, t))
    A = keep
    print("alignment anchors from English-mode timing:", len(A), "of", len(words), "caption words")

# ---- anchor the captions to words Whisper heard at exact times (fixes captions running ahead of speech) ----
ANCH = [("let's", 20.46), ("video", 21.22), ("92", 29.00), ("five", 33.20), ("45", 38.96), ("six", 41.52), ("aptitude", 70.80), ("verbal", 71.70),
        ("java", 72.68), ("dbms", 73.66), ("java", 86.5), ("oracle", 87.3), ("react", 88.6), ("performance", 89.3), ("second", 94.5), ("software", 95.9), ("third", 99.7), ("ais", 101.5), ("windows", 102.2), ("networking", 102.8), ("generic", 110.50), ("java", 111.94), ("hsql", 112.94), ("45", 130.30), ("java", 131.06),
        ("performance", 131.52), ("jmeter", 134.52), ("front-end", 135.66), ("six", 188.16), ("3", 188.94), ("lpa", 189.56),
        ("65", 195.48), ("70", 199.72), ("80", 203.76), ("information", 287.88)]
def norm(x):
    return re.sub(r"[^\w\-']", "", x.lower())
fixed = []  # (idx, time)
ptr = -1
report = []
for tok, t in ANCH:
    cand = [i for i in range(ptr + 1, len(words)) if norm(words[i][2]) == tok and abs(words[i][0] - t) < 12]
    if not cand:
        report.append((tok, t, None)); continue
    i = min(cand, key=lambda i: abs(words[i][0] - t))
    if fixed and t <= fixed[-1][1]:
        continue
    report.append((tok, t, words[i][0] - t))
    fixed.append((i, t)); ptr = i
if A:
    fixed = list(A)
print("anchors used:", len(fixed), "of", len(ANCH))
print("shift before correction (caption time minus real time), seconds:", ", ".join(f"{tok}:{d:+.1f}" for tok, t, d in report if d is not None))
if fixed:
    hard = list(fixed)
    hidx = {i for i, _ in hard}
    soft_ok = 0
    for i, t in ([] if A else seg_first):
        if i in hidx or i == 0:
            continue
        prev = [h for h in hard if h[0] < i]
        nxt = [h for h in hard if h[0] > i]
        if prev and t <= prev[-1][1] + 0.3:
            continue
        if nxt and t >= nxt[0][1] - 0.3:
            continue
        fixed.append((i, t)); soft_ok += 1
    fixed.sort()
    # keep times strictly increasing
    keep = []
    for i, t in fixed:
        if keep and t <= keep[-1][1] + 0.05:
            continue
        keep.append((i, t))
    fixed = keep
    print("segment-start anchors added:", soft_ok, "total anchors:", len(fixed))
    old = [w[0] for w in words]
    pts = [(0, min(old[0], fixed[0][1] - 0.01))] + fixed + [(len(words) - 1, max(old[-1], fixed[-1][1] + 0.5))]
    L = [len(w[2]) + 1 for w in words]
    for (ia, ta), (ib, tb) in zip(pts, pts[1:]):
        if ib <= ia:
            continue
        tot = sum(L[ia:ib]) or 1
        acc = 0
        for k in range(ia, ib):
            words[k][0] = ta + (tb - ta) * acc / tot
            acc += L[k]
        words[ib][0] = tb
    for i in range(len(words)):
        nxt = words[i + 1][0] if i + 1 < len(words) else words[i][0] + 1.0
        words[i][1] = min(nxt, words[i][0] + 1.4)

for i in range(len(words) - 1):  # monotonic starts, no overlaps
    if words[i + 1][0] < words[i][0] + 0.05:
        words[i + 1][0] = words[i][0] + 0.05
    if words[i][1] > words[i + 1][0]:
        words[i][1] = words[i + 1][0]

def ts(x):
    h = int(x // 3600); m = int((x % 3600) // 60); s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"

try:
    THEME = json.load(open("animations/slot_scenes/theme.json"))
except Exception:
    THEME = {}
_h = THEME.get("accent_light", "#ff6b7d").lstrip("#")
RED = "&H%s%s%s&" % (_h[4:6].upper(), _h[2:4].upper(), _h[0:2].upper())  # caption highlight = theme accent_light (ASS uses BGR)
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,__SANS__,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,0,3,2,80,80,70,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
lines = []
CH = 4
chunks, cur = [], []
for w in words:
    if cur and (len(cur) >= CH or w[0] - cur[-1][1] > 0.8):  # never group words across a pause (music, silence)
        chunks.append(cur); cur = []
    cur.append(w)
if cur:
    chunks.append(cur)
for ci, chunk in enumerate(chunks):
    nxt_chunk = chunks[ci + 1][0][0] if ci + 1 < len(chunks) else 1e9
    for i, w in enumerate(chunk):
        st = w[0]
        if i + 1 < len(chunk):
            en = min(chunk[i + 1][0], w[1] + 0.6)
        else:
            en = min(nxt_chunk, w[1] + 0.25)
        txt = " ".join((("{\\c%s}%s{\\c&HFFFFFF&}" % (RED, x[2])) if j == i else x[2]) for j, x in enumerate(chunk))
        skip = False
        for pa, pb in PROT:
            if pa <= st < pb:
                skip = True
            elif st < pa < en:
                en = pa
        if skip:
            continue
        lines.append(f"Dialogue: 0,{ts(st)},{ts(max(en, st + 0.08))},Cap,,0,0,0,,{txt}")
open("captions.ass", "w", encoding="utf-8").write((head + "\n".join(lines) + "\n").replace("__SANS__", THEME.get("sans", "Inter Tight")))
print("captions:", len(words), "words,", len(lines), "dialogue lines")

if os.environ.get("CAPTIONS_ONLY"):
    sys.exit(0)
# ---- final compose ----
# One overlay track in time order (transparent gaps between scenes) so frames flow sequentially and memory stays small.
# ---- gentle zoom (only while the speaker is on screen) + light colour grade on the speaker footage ----
ZMAX = 1.07
zsegs = []
prev_end = 0.0
ramp = 0
for sid, t in sorted(T.items(), key=lambda kv: kv[1]):
    a, b = prev_end, t
    if b - a >= 4.0:
        z0, z1 = (1.0, ZMAX) if ramp % 2 == 0 else (ZMAX, 1.0)
        ramp += 1
    else:
        z0 = z1 = 1.0
    zsegs.append((a, b, z0, z1))
    prev_end = t + ST[sid]["dur"]
a, b = prev_end, DUR_TOTAL
z0, z1 = (1.0, ZMAX) if ramp % 2 == 0 else (ZMAX, 1.0)
zsegs.append((a, b, z0, z1))
def zseg(a, b, z0, z1):
    return f"{z0}+({z1 - z0:.4f})*min(max((t-{a:.3f})/{max(b - a, 0.001):.3f},0),1)"
Z = zseg(*zsegs[-1])
for a, b, z0, z1 in reversed(zsegs[:-1]):
    Z = f"if(lt(t,{b + 0.3:.3f}),{zseg(a, b, z0, z1)},{Z})"
NOPROT = "*".join(f"not(between(t,{pa},{pb}))" for pa, pb in PROT) or "1"
GRADE = f"eq=contrast=1.06:saturation=1.10:enable='{NOPROT}',unsharp=5:5:0.35:5:5:0:enable='{NOPROT}'"
ZP = Z
for pa, pb in PROT:
    ZP = f"if(between(t,{pa},{pb}),1,{ZP})"
base = (f"[0:v]scale=w='trunc({W}*({ZP})/2)*2':h='trunc({H}*({ZP})/2)*2':eval=frame:flags=lanczos,"
        f"crop={W}:{H}:x='(iw-{W})*0.43':y='(ih-{H})*0.36',setsar=1,{GRADE},"
        "ass=captions.ass:fontsdir=../../../brand/fonts/approved[base]")
chain = [base]
segs = []
prev_end = 0.0
order = sorted(T.items(), key=lambda kv: kv[1])
for i, (sid, t) in enumerate(order):
    off, d = OFF[sid]
    gap = max(0.0, t - prev_end)
    if gap > 0.001:
        chain.append(f"color=c=black@0.0:s={W}x{H}:r=30:d={gap:.3f},format=yuva420p,setsar=1[g{i}]")
        segs.append(f"[g{i}]")
    chain.append(f"[1:v]trim=start={off}:duration={d},setpts=PTS-STARTPTS,fps=30,format=yuva420p,setsar=1,fade=t=in:st=0:d={FADE}:alpha=1,fade=t=out:st={d - FADE}:d={FADE}:alpha=1[sc{i}]")
    segs.append(f"[sc{i}]")
    prev_end = t + d
tail = DUR_TOTAL - prev_end
if tail > 0.001:
    chain.append(f"color=c=black@0.0:s={W}x{H}:r=30:d={tail + 1:.3f},format=yuva420p,setsar=1[gend]")
    segs.append("[gend]")
chain.append("".join(segs) + f"concat=n={len(segs)}:v=1:a=0[ov]")
chain.append("[base][ov]overlay=format=auto:eof_action=pass[vout]")
chain.append("[0:a][2:a]amix=inputs=2:normalize=0:duration=first:dropout_transition=0[aout]")
open("filter_debug.txt", "w").write(";\n".join(chain))
out = sys.argv[1] if len(sys.argv) > 1 else "preview_v1.mp4"
cmd = ["nice", "-n", "10", "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", SRC, "-i", SCENES, "-i", "sfx_track.wav",
       "-filter_complex", ";".join(chain), "-map", "[vout]", "-map", "[aout]",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", ("19" if RES4K else "21"), "-pix_fmt", "yuv420p", "-r", "30",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-t", os.environ.get("TEST_T", f"{DUR_TOTAL:.3f}"), out]
subprocess.run(cmd, check=True)
print("wrote", out)
