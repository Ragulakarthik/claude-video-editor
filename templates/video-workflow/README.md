# Video workflow (the same for EVERY video; only the theme changes)
The full step list lives in ../../CLAUDE.md ("Workflow: EVERY video follows these steps"). This folder holds the reusable parts.

Start: `python3 templates/video-workflow/new_video.py <slug>`

| File | What it does |
|---|---|
| files/slot/theme.json | THE ONLY THING THAT CHANGES: accent colours, ink, ground, font names and files |
| files/slot/build_scenes.py | the screens (edit the SC list per video) -> index.html + scene_times.json for HyperFrames |
| files/en_timing.py | English-mode Whisper over the whole video -> exact word times (transcripts/timing_en.json) |
| files/find_protected.py | finds the user's own intro animation / end screen -> protected.json |
| files/compose.py | zoom + grade + captions (matched to the word times) + sound effects + scenes -> preview/final |
| files/make_thumbnail.py | 1280x720 thumbnails from a frame + text, in the video's theme |
| files/publish_template.md | titles, tags (comma separated, under 500 characters), hashtags, chapters |

Hard-won rules: time every screen from English-mode word times (not chapter times); use one overlay track with transparent gaps (not one overlay per scene, it runs out of memory); keep the user's intro/end screen untouched; run long jobs with run_in_background and stop them with TaskStop.
