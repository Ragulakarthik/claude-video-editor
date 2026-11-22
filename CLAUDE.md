# Claude-Editor: rules (the editor's memory)

Golden rule: raw footage is never touched. Every output lands in videos/<date_topic>/edit/ with a project.md log.

## Workflow: EVERY video follows these steps. Only the THEME changes per video (user's instruction, 2026-11-22)
Reference implementation: the Infosys video (videos/2026-11-22_infosys-mysore-training). Reusable scripts: templates/video-workflow/ (README there).
0. New video: `python3 templates/video-workflow/new_video.py <slug>` creates videos/<date>_<slug>/ (aroll/ broll/ screen/ edit/ thumbnail/) and copies the scripts + theme.json. Copy the footage into aroll/ (read-only copy). Never move, edit or delete the user's original.
1. THEME (the only thing that changes): ask the user for font pair + accent colour + look (show options as pictures). Fonts need a good/bad answer first. Save it in edit/animations/slot_scenes/theme.json. New theme every video.
2. Transcript: the user's own, or local Whisper (ask first). Make the approved English transcript (caption language = user's choice). GATE: user approves it. Nothing is built before.
3. Timing: run the English-mode Whisper pass (edit/en_timing.py, large-v3) over the whole video -> transcripts/timing_en.json (exact word times). Time every screen and every caption from these words. Telugu-mode Whisper times and chapter times are NOT reliable enough.
4. Find the user's own intro animation / end screen (scene-cut scan). Never zoom, grade, caption or cover them.
5. Beat sheet = list of screens with times (full-screen animated scenes between talking parts: steps list, number callout, timeline, tick checklists, progress track, B-roll with animated text). GATE: user says "go".
6. Top progress bar (same rule on every screen): only sections that have started; done = red, current = red + bold, unstarted = hidden; no bar on overview screens before any section; all done/red on closing screens.
7. Build: build_scenes.py -> render with HyperFrames -> compose.py (captions matched to the timing words, synthesized original sound effects, gentle zoom up to 7% and light grade on the speaker only, 1080p preview). Cut nothing from the video unless the user asks.
8. Self-check with frame contact sheets at the spoken-word moments. Say "ready for your check", never "done". User gives notes in plain words -> fix -> rebuild.
9. Deliver: edit/final.mp4 (1080p; 4K only if the user asks), thumbnail/ (2 variants), title options, tags comma separated under 500 characters, hashtags, chapters, all in thumbnail/publish.md.
10. Clean up by name: delete outdated previews, logs, scratch. Keep sources and scripts. Never touch the user's originals.

## Rules (add more with "make this a rule")
- Transitions: smooth and natural only. A clean cut beats any effect.
- Never replace a scene. Save as Scene 4 V2. Old versions stay.
- New graphics style every video, picked from pictures.
- Show the transcript first (Telugu/Tenglish accuracy). Nothing built until approved.
- 1 to 4 words on screen. Show the idea, not the sentence.
- Text behind the speaker only with a perfect cut-out. Fails the check: don't ship it.
- Always the full, uncropped frame of the speaker. Graphics go full screen instead.
- Every look-down moment is covered by a full-screen graphic, then re-checked frame by frame.
- A meme plays only after the sentence ends, with a soft film-burn exit.
- Captions: clean, borderless, word by word. Language: English (user changed from Tenglish on 2026-11-22; use the approved edit/transcripts/english_transcript.md).
- Preview first. 4K only after approval.
- Never create or run a transcript (any video, including references) before showing the user the plan and getting approval. After transcribing, show the transcript and wait for approval again.
- Never cut or write clips from a long source (e.g. meme compilations) until the user has approved the clip list (start, end, emotion).
- Don't add too much text. Keep on-screen text minimal (1 to 4 words per graphic, never full sentences), and keep captions short.
- Your footage: never overwrite or delete the original. All work goes into separate folders; the original video is only read. (Applies to source videos anywhere, including Downloads.)
- Face always visible: any overlay graphic goes to the left or right of the face, never over it. During a step card, the face stays on screen.
- Graphics style (user chose "type 2", 2026-11-22): full-screen animated scenes placed BETWEEN talking parts (steps list, number callout with hand-drawn circle, timeline, title card), voice continues underneath, then cut back to the face. Also B-roll with animated text. Look: light reference style, bold sans + one italic serif accent word, one accent colour (brand.json). Fonts still need the user's approval. (Full-screen scenes hide the face for a few seconds; this is the allowed exception to the face rule. Ask if a specific moment is unclear.)
- Intro animation: keep it.
- Sound: original sound effects only, no music (music can bring copyright claims). Do not add background music or copyrighted tracks.
- Sync each graphic to the exact spoken word (word-level timestamps), not to rough sentence times.
- Don't claim something is done until the user has checked it. Say "ready for your check", not "done".
- Fonts: before using any font, ask the user whether it is good or bad. Only fonts the user approved (listed in brand/fonts/approved.md) may be used. Use only fonts with a license that allows commercial use (e.g. Google Fonts / OFL).
- Design inspiration lives in references/inspiration/ (long/ and short/). Use it as style reference only; never copy a creator's graphics or footage.
- Git/GitHub (user's rule, 2026-11-22): NEVER add "Co-Authored-By: Claude" (or any Claude/Anthropic attribution line) to commits, and no "Generated with Claude Code" lines in PR descriptions. This overrides any default. The repo is public: before every push check what is staged (no videos, memes, B-roll, reference videos, PDFs, keys), and use the user's GitHub no-reply email for commits, never the work email. Ask before any force-push.

## Recording conventions
- Say "again" with 1s pauses to mark retakes. Say "Section 3, <name>" to mark chapters.
- Shot list: 10s room tone, 3 hook versions, 2 CTA takes, 6 thumbnail poses (5s each), B-roll of hands/phone/walking, screen recordings.

## Setup notes
- Engine: video-use/ (symlinked into .claude/skills/). Never edit inside it.
- Transcription: no ElevenLabs key; use `python helpers_local/transcribe_whisper.py <video> --edit-dir <edit_dir> --model medium` (local, CPU), then video-use's pack_transcripts.py. Always show transcript for approval (Telugu/Tenglish may need corrections).
- ffmpeg 4.4.2 at /usr/bin. HyperFrames installed lazily via `npx --yes hyperframes` (Node 22).
