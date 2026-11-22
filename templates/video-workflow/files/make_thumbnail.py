"""Makes a 1280x720 thumbnail: a frame of the speaker on the left, big text on the right (never over the face), in the video's THEME.
Run from the edit/ folder:
    python3 make_thumbnail.py --time 47 --big "INFOSYS" --italic "training" --pill "3.6 or 3 LPA?" --name A
Writes ../thumbnail/thumbnail_<name>.png and .jpg (JPG is under 2 MB, ready for upload).
--pill may contain <i>word</i> for an italic serif word. Use --big2 for a second white line (variant B style).
"""
import argparse, glob, json, os, subprocess, tempfile, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--cutout", default="", help="use a picture of the speaker with a transparent background (png) instead of a video frame")
ap.add_argument("--cutout-scale", type=float, default=1.7)
ap.add_argument("--cutout-x", type=int, default=-50)
ap.add_argument("--time", type=float, default=0.0, help="second of the speaker footage to use (pick one with eyes on camera)")
ap.add_argument("--big", required=True)
ap.add_argument("--italic", default="")
ap.add_argument("--big2", default="")
ap.add_argument("--pill", default="")
ap.add_argument("--name", default="A")
ap.add_argument("--offset-x", type=int, default=-320, help="shift the frame left so the face sits on the left third")
a = ap.parse_args()

T = {"accent": "#D7263D", "accent_light": "#ff6b7d", "sans": "Inter Tight", "serif": "Instrument Serif",
     "sans_file": "InterTight.ttf", "serif_italic_file": "InstrumentSerif-Italic.ttf"}
tf = "animations/slot_scenes/theme.json"
if os.path.exists(tf):
    T.update(json.load(open(tf)))
src = sorted(glob.glob("../aroll/*.mp4"))[0]
out_dir = os.path.join("..", "thumbnail")
os.makedirs(out_dir, exist_ok=True)
work = tempfile.mkdtemp(prefix="thumb_")
fonts = os.path.join(work, "fonts")
os.makedirs(fonts)
for f in (T["sans_file"], T["serif_italic_file"]):
    shutil.copy(os.path.join("animations/slot_scenes/assets/fonts", f), fonts)
if a.cutout:
    shutil.copy(a.cutout, os.path.join(work, "cutout.png"))
else:
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", str(a.time), "-i", src, "-frames:v", "1", os.path.join(work, "frame.png")], check=True)

body = f'<div class="a">{a.big}</div>'
if a.italic:
    body += f'<div class="b">{a.italic}</div>'
if a.big2:
    body += f'<div class="a" style="font-size:96px;margin-top:6px">{a.big2}</div>'
if a.pill:
    body += f'<div class="pill">{a.pill}</div>'
def rgba(hexc, al):
    h = hexc.lstrip("#")
    return "rgba(%d,%d,%d,%s)" % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), al)

if a.cutout:
    from PIL import Image as _I
    cw, ch = _I.open(a.cutout).size
    W_, H_ = int(cw * a.cutout_scale), int(ch * a.cutout_scale)
    stage = (f'<div class="bg"></div><img class="cut" src="cutout.png" style="left:{a.cutout_x}px;top:{720 - H_}px;width:{W_}px;height:{H_}px">')
    txt_css = ".txt{position:absolute;left:730px;top:80px;width:520px;color:#fff}.a{font-size:112px}.b{font-size:122px}.pill{font-size:56px}.pill i{font-size:66px}"
    bg_css = (f".bg{{position:absolute;inset:0;background:radial-gradient(circle at 24% 58%,{rgba(T['accent'], .45)} 0%,transparent 52%),"
              f"linear-gradient(135deg,{T.get('ink', '#14171c')} 0%,#0b0d11 100%)}}.cut{{position:absolute}}")
else:
    stage = '<img src="frame.png"><div class="shade"></div>'
    txt_css = ".txt{position:absolute;left:640px;top:70px;width:600px;color:#fff}"
    bg_css = (f"img{{position:absolute;left:{a.offset_x}px;top:-45px;width:1600px;height:900px}}"
              ".shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(12,15,20,0) 28%,rgba(12,15,20,.78) 52%,rgba(12,15,20,.92) 100%)}")
html = f"""<!doctype html><meta charset="utf-8"><style>
@font-face{{font-family:'{T['sans']}';src:url(fonts/{T['sans_file']});font-weight:100 900}}
@font-face{{font-family:'{T['serif']}';src:url(fonts/{T['serif_italic_file']});font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:1280px;height:720px;overflow:hidden;background:#111}}
.wrap{{position:relative;width:1280px;height:720px;overflow:hidden;font-family:'{T['sans']}'}}
{bg_css}
{txt_css}
.a{{font-weight:800;font-size:128px;line-height:.92;letter-spacing:-.04em}}
.b{{font-family:'{T['serif']}';font-style:italic;font-weight:400;font-size:138px;line-height:.95;color:{T['accent_light']};letter-spacing:-.01em}}
.pill{{display:inline-block;margin-top:34px;background:{T['accent']};color:#fff;font-weight:800;font-size:64px;padding:8px 34px;border-radius:99px;letter-spacing:-.02em}}
.pill i{{font-family:'{T['serif']}';font-weight:400;font-size:74px}}
</style><div class="wrap">{stage}<div class="txt">{body}</div></div>"""
hp = os.path.join(work, "t.html")
open(hp, "w").write(html)
raw = os.path.join(work, "raw.png")
subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox", "--hide-scrollbars", "--window-size=1280,900",
                "--virtual-time-budget=5000", f"--screenshot={raw}", "file://" + hp], capture_output=True, timeout=120)
from PIL import Image
im = Image.open(raw).convert("RGB").crop((0, 0, 1280, 720))
im.save(os.path.join(out_dir, f"thumbnail_{a.name}.png"))
im.save(os.path.join(out_dir, f"thumbnail_{a.name}.jpg"), quality=92)
shutil.rmtree(work)
print("wrote", os.path.join(out_dir, f"thumbnail_{a.name}.jpg"), os.path.getsize(os.path.join(out_dir, f"thumbnail_{a.name}.jpg")), "bytes")
