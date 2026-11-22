"""Finds the user's own intro animation / end screen: hard visual cuts in the speaker footage. Prints cut times; the intro is the
cluster of cuts near the start, the end screen is the cut near the end. Check frames, then write edit/protected.json = [[start, end], ...]."""
import glob, os, re, subprocess
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = sorted(glob.glob("../aroll/*.mp4"))[0]
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-vf", "select='gt(scene,0.25)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True)
print("hard cuts (seconds):", [float(x) for x in re.findall(r"pts_time:([0-9.]+)", r.stderr)])
print("A talking-head video should have very few. Cuts near 0-30 s and the last 10 s are usually the intro and end screen.")
