"""Starts a new video the standard way.   python3 templates/video-workflow/new_video.py <slug> [--date YYYY-MM-DD]
Creates videos/<date>_<slug>/ with aroll/ broll/ screen/ edit/ thumbnail/, copies the scripts, the theme file, the sound effects
and the approved fonts. The THEME (edit/animations/slot_scenes/theme.json) is the only thing you change per video."""
import argparse, datetime, json, os, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")
ap = argparse.ArgumentParser()
ap.add_argument("slug")
ap.add_argument("--date", default=datetime.date.today().isoformat())
a = ap.parse_args()
dest = os.path.join(ROOT, "videos", f"{a.date}_{a.slug}")
if os.path.exists(dest):
    raise SystemExit(f"already exists: {dest}")
slot = os.path.join(dest, "edit", "animations", "slot_scenes")
for d in ("aroll", "broll", "screen", "thumbnail", "edit/transcripts", "edit/sfx", "edit/animations/slot_scenes/assets/fonts"):
    os.makedirs(os.path.join(dest, d))
for f in ("compose.py", "en_timing.py", "find_protected.py", "make_thumbnail.py"):
    shutil.copy(os.path.join(F, f), os.path.join(dest, "edit", f))
for f in os.listdir(os.path.join(F, "slot")):
    shutil.copy(os.path.join(F, "slot", f), os.path.join(slot, f))
meta = json.load(open(os.path.join(slot, "meta.json")))
meta.update({"id": a.slug, "name": a.slug})
json.dump(meta, open(os.path.join(slot, "meta.json"), "w"))
theme = json.load(open(os.path.join(slot, "theme.json")))
for f in os.listdir(os.path.join(ROOT, "brand", "sfx")):
    if f.endswith(".wav"):
        shutil.copy(os.path.join(ROOT, "brand", "sfx", f), os.path.join(dest, "edit", "sfx", f))
missing = []
for k in ("sans_file", "serif_italic_file", "serif_regular_file"):
    ad = os.path.join(ROOT, "brand", "fonts", "approved")
    src = os.path.join(ad, theme[k])
    if not os.path.exists(src):  # variable fonts are saved like InterTight[wght].ttf: match ignoring the [..] part
        import re
        hits = [f for f in os.listdir(ad) if re.sub(r"\[.*?\]", "", f) == theme[k]]
        src = os.path.join(ad, hits[0]) if hits else src
    if os.path.exists(src):
        shutil.copy(src, os.path.join(slot, "assets", "fonts", theme[k]))
    else:
        missing.append(theme[k])
open(os.path.join(dest, "project.md"), "w").write(f"# Project log: {a.slug}\n- {a.date}: created with templates/video-workflow/new_video.py. Status: waiting for footage and the THEME.\n")
shutil.copy(os.path.join(F, "publish_template.md"), os.path.join(dest, "thumbnail", "publish.md"))
p = os.path.join(dest, "thumbnail", "publish.md")
open(p, "w").write(open(p).read().replace("__SLUG__", a.slug))
print("created", dest)
if missing:
    print("NOTE: theme fonts not in brand/fonts/approved yet (ask the user good/bad first):", missing)
print("""next:
 1. copy the footage into aroll/ (read-only copy; never touch the original)
 2. ask the user for the THEME (fonts + accent + look), edit edit/animations/slot_scenes/theme.json
 3. transcript -> user approves -> English-mode timing: python3 edit/en_timing.py
 4. python3 edit/find_protected.py -> write edit/protected.json for the user's intro / end screen
 5. beat sheet -> user says go -> edit build_scenes.py (SC list) -> python3 build_scenes.py -> render -> python3 compose.py
 6. thumbnails: python3 edit/make_thumbnail.py ...  and fill thumbnail/publish.md""")
