"""Checks that everything this workflow needs is installed and tells you how to fix what is missing.
    python3 check_setup.py            quick check
    python3 check_setup.py --doctor   also runs the HyperFrames doctor (needs internet the first time)
"""
import os
import platform
import re
import shutil
import subprocess
import sys

OS = platform.system()  # Linux, Darwin (macOS) or Windows
problems = []


def hint(linux, mac, win):
    return {"Linux": linux, "Darwin": mac, "Windows": win}.get(OS, linux)


def ok(name, detail=""):
    print(f"  OK       {name} {detail}".rstrip())


def bad(name, fix):
    print(f"  MISSING  {name}\n           fix: {fix}")
    problems.append(name)


def version_of(cmd, pattern=r"(\d+)\.(\d+)"):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        m = re.search(pattern, out.stdout + out.stderr)
        return (int(m.group(1)), int(m.group(2))) if m else None
    except Exception:
        return None


def find_chrome():
    if os.environ.get("CHROME_PATH") and os.path.exists(os.environ["CHROME_PATH"]):
        return os.environ["CHROME_PATH"]
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        if shutil.which(n):
            return shutil.which(n)
    for p in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
        if os.path.exists(p):
            return p
    return None


print(f"System: {OS}, Python {platform.python_version()}\n")

if sys.version_info >= (3, 10):
    ok("Python 3.10+")
else:
    bad("Python 3.10 or newer", "https://www.python.org/downloads/")

for mod, pkg in (("faster_whisper", "faster-whisper"), ("PIL", "pillow")):
    try:
        __import__(mod)
        ok(f"Python package {pkg}")
    except ImportError:
        bad(f"Python package {pkg}", "pip install -r requirements.txt")

for tool in ("ffmpeg", "ffprobe"):
    if shutil.which(tool):
        v = version_of([tool, "-version"])
        ok(tool, f"{v[0]}.{v[1]}" if v else "")
    else:
        bad(tool, hint("sudo apt install ffmpeg", "brew install ffmpeg", "winget install ffmpeg"))

if shutil.which("node"):
    v = version_of(["node", "-v"])
    if v and v[0] >= 22:
        ok("Node.js 22+", f"({v[0]}.{v[1]})")
    else:
        bad("Node.js 22 or newer (HyperFrames needs it)", "https://nodejs.org  or  nvm install 22")
else:
    bad("Node.js 22 or newer", "https://nodejs.org  or  nvm install 22")

if shutil.which("npx"):
    ok("npx")
else:
    bad("npx (comes with Node.js)", "install Node.js 22+ from https://nodejs.org")

chrome = find_chrome()
if chrome:
    ok("Google Chrome", f"({chrome})")
else:
    bad("Google Chrome", "https://www.google.com/chrome/  (or set CHROME_PATH to its full path)")

fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand", "fonts", "approved")
if os.path.isdir(fonts_dir) and any(f.lower().endswith((".ttf", ".otf")) for f in os.listdir(fonts_dir)):
    ok("Approved fonts in brand/fonts/approved/")
else:
    print("  NOTE     no fonts in brand/fonts/approved/ yet: download your theme's fonts from https://fonts.google.com and list them in brand/fonts/approved.md")

if "--doctor" in sys.argv and shutil.which("npx"):
    print("\nRunning the HyperFrames doctor...\n")
    subprocess.run(["npx", "--yes", "hyperframes@0.9.81", "doctor"])

print()
if problems:
    print(f"{len(problems)} thing(s) missing: {', '.join(problems)}")
    sys.exit(1)
print("Everything needed is installed.")
