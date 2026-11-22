# Claude Video Editor

A repeatable way to edit talking-head videos by talking to Claude Code: transcript, exact word timing, animated full-screen scenes,
captions, original sound effects, a gentle zoom and grade, then thumbnail, title and tags.
**Every video follows the same steps. Only the theme (fonts, accent colour, look) changes.**

## What is in this repo
| Path | What it is |
|---|---|
| `CLAUDE.md` | the rules and the 10-step workflow Claude follows for every video |
| `templates/video-workflow/` | reusable scripts + `new_video.py` that sets up a new video folder |
| `templates/video-workflow/files/slot/theme.json` | the only thing that changes per video: colours and fonts |
| `helpers_local/transcribe_whisper.py` | local Whisper transcription (nothing is uploaded) |
| `brand/` | brand settings, the font approval list, original synthesized sound effects (no music) |

## How it works
1. `python3 templates/video-workflow/new_video.py <name>` creates `videos/<date>_<name>/` (`aroll/ broll/ screen/ edit/ thumbnail/`).
2. Copy your footage into `aroll/` (a copy; the original is never touched). Choose the theme in `theme.json`.
3. Transcript, approved by you. Then `edit/en_timing.py` runs Whisper (large-v3, English mode) over the whole video for exact word times.
4. `edit/find_protected.py` finds your own intro animation and end screen so they are never zoomed, graded or captioned.
5. Screens are described in `build_scenes.py`, rendered with [HyperFrames](https://github.com/heygen-com/hyperframes), and put together by `compose.py`
   (captions matched to the word times, sound effects, zoom up to 7%, light grade, 1080p).
6. `edit/make_thumbnail.py` makes 1280x720 thumbnails; `thumbnail/publish.md` holds titles, tags (comma separated, under 500 characters), hashtags and chapters.

## Requirements
ffmpeg and ffprobe, Python 3.10+ (`faster-whisper`, `pillow`), Node 22+ (HyperFrames runs through `npx`), Google Chrome.
Fonts: download your theme's fonts from Google Fonts (they are open licence) into `brand/fonts/approved/` and list them in `brand/fonts/approved.md`.

## Not included on purpose
Videos, meme clips, stock B-roll and reference videos (copyright and size). The workflow keeps them in `videos/`, `memes/`, `broll-library/` and
`references/`, which are git-ignored.

## Credits
Inspired by the "Your editor is Claude" field guide and the open-source `video-use` and HyperFrames projects.
