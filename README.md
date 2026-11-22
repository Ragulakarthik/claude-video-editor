# Claude Video Editor

A repeatable way to edit talking-head videos by talking to Claude Code: transcript, exact word timing, animated full-screen scenes,
captions, original sound effects, a gentle zoom and grade, then thumbnail, title and tags.
**Every video follows the same steps. Only the theme (fonts, accent colour, look) changes.**

You give Claude your raw video. Claude does the editing with the scripts in this repo, and you approve each gate
(transcript, plan, preview) before it goes on.

## What is in this repo
| Path | What it is |
|---|---|
| `CLAUDE.md` | the rules and the 10-step workflow Claude follows for every video |
| `templates/video-workflow/` | reusable scripts + `new_video.py` that sets up a new video folder |
| `templates/video-workflow/files/slot/theme.json` | the only thing that changes per video: colours and fonts |
| `helpers_local/transcribe_whisper.py` | local Whisper transcription (nothing is uploaded) |
| `brand/` | brand settings, the font approval list, original synthesized sound effects (no music) |
| `requirements.txt` | the Python packages |

## What to install
You need a **paid Claude plan with Claude Code** (desktop app "Code" tab, or the CLI: `npm install -g @anthropic-ai/claude-code`).
Then these tools (Claude can install most of them for you if you use the prompt below):

| Tool | Version | Install |
|---|---|---|
| ffmpeg + ffprobe | 4.4 or newer | Ubuntu/Debian: `sudo apt install ffmpeg` · macOS: `brew install ffmpeg` · Windows: `winget install ffmpeg` |
| Python | 3.10 or newer | https://www.python.org/downloads/ |
| Python packages | | `pip install -r requirements.txt` (faster-whisper, pillow) |
| Node.js | **22 or newer** (HyperFrames needs it) | https://nodejs.org or `nvm install 22` |
| Google Chrome | any recent | https://www.google.com/chrome/ (HyperFrames renders the graphics with it) |
| HyperFrames | pinned in `package.json` | nothing to install: it runs through `npx --yes hyperframes@0.9.81 ...` |
| Fonts | | download your theme's fonts from [Google Fonts](https://fonts.google.com) (open licence) into `brand/fonts/approved/` and list them in `brand/fonts/approved.md` |

Good to know:
- The first Whisper run downloads the `large-v3` model (about 3 GB). On a CPU it is slow (many minutes for a 5-minute video); a GPU is faster.
- Keep about 5 GB free per video for previews and renders.
- Check your setup:
  ```
  ffmpeg -version | head -1 && node -v && python3 -c "import faster_whisper, PIL; print('python ok')" && google-chrome --version
  npx --yes hyperframes@0.9.81 doctor
  ```

## Give this prompt to your Claude Code
Open a folder where you want to work, start Claude Code there, and paste this (fill in the three `<...>` parts):

```
You are my video editor. Set up and use this repo: https://github.com/Ragulakarthik/claude-video-editor

1. Clone it into a folder called Claude-Editor and work inside it. Read CLAUDE.md and
   templates/video-workflow/README.md first. CLAUDE.md holds the original author's personal preferences:
   ask me which rules I want to keep or change before we start, then follow the workflow in CLAUDE.md for every video.
2. Check what is installed: ffmpeg and ffprobe, Python 3.10+, faster-whisper and pillow (pip install -r requirements.txt),
   Node 22+, Google Chrome. Install what is missing. If a step needs sudo, show me the exact command and let me run it.
   Then run: npx --yes hyperframes@0.9.81 doctor and fix any real problem.
3. Theme: ask me for my fonts (a bold sans + one italic serif works well), my accent colour and the look I want.
   Tell me each font's licence and wait for my "good" or "bad" before using it. Download approved fonts from Google Fonts
   into brand/fonts/approved/ and write my choices into the theme.json of the new video.
4. Run: python3 templates/video-workflow/new_video.py <my-video-name>
   Copy my raw video into that video's aroll/ folder as a copy. Never move, edit or delete my original.
5. Then follow the workflow: ask before you transcribe anything, show me the transcript and wait for my approval,
   find my own intro or end screen and leave them untouched, show me the plan, wait for my "go", build a preview,
   and tell me "ready for your check", never "done", until I have watched it.
Rules for everything: never cut my video unless I ask; no background music (original sound effects only);
never add Claude as co-author to a git commit; ask before pushing anything to GitHub.

My raw video: <full path to my video file>
The language I speak in the video: <language>
Captions language: <English or the same language>
```

## How it works (what Claude does with the scripts)
1. `python3 templates/video-workflow/new_video.py <name>` creates `videos/<date>_<name>/` (`aroll/ broll/ screen/ edit/ thumbnail/`).
2. Your footage goes into `aroll/` (a copy; the original is never touched). You choose the theme in `theme.json`.
3. Transcript, approved by you. Then `edit/en_timing.py` runs Whisper (large-v3, English mode) over the whole video for exact word times.
4. `edit/find_protected.py` finds your own intro animation and end screen so they are never zoomed, graded or captioned.
5. Screens are described in `build_scenes.py`, rendered with [HyperFrames](https://github.com/heygen-com/hyperframes), and put together by `compose.py`
   (captions matched to the word times, sound effects, zoom up to 7%, light grade, 1080p).
6. `edit/make_thumbnail.py` makes 1280x720 thumbnails; `thumbnail/publish.md` holds titles, tags (comma separated, under 500 characters), hashtags and chapters.

## Limits (honest)
- Claude Code does the thinking (which screens, what to write). Without it you would write the scene list by hand.
- It was built and tested end to end on one talking-head video (a person centred in front of a plain wall, 16:9). Other framings may need small changes
  (the zoom and thumbnail framing are tuned for a centred speaker).
- Licensed under the MIT licence (see `LICENSE`). It covers the code and docs in this repo, not the tools it uses (ffmpeg, Whisper, HyperFrames, Claude Code) or your own videos and fonts, which keep their own licences.

## Not included on purpose
Videos, meme clips, stock B-roll and reference videos (copyright and size). The workflow keeps them in `videos/`, `memes/`, `broll-library/` and
`references/`, which are git-ignored.
