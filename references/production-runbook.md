# Production runbook

This is the operational sequence for a new topic. It is intentionally parameterized; the Opus 5.5 constants are examples, not defaults to preserve.

This runbook describes the HTML/Playwright renderer. For a 3D React composition, follow [the Remotion route](remotion-route.md) for preview/render, then use the same independent MP4 checks in step 5. The [narrative route](narrative-explainers.md) adds subtitle and claim checks when the film is an explainer.

## 1. Lock one timeline

Choose `fps`, `bpm`, `total_frames`, aspect ratio and scene boundaries before animation or sound. Store boundaries as integer frame indices and derive seconds by division. A beat is `60 / bpm` seconds; at 30 fps and 120 BPM it is exactly 15 frames. When beat length is fractional in frames, round event positions once in the plan and use those exact indices throughout. Check every `start_frame` equals the previous scene's end and the final end equals `total_frames`.

Write the spoken or on-screen copy and the music hit map beside those indices. Reserve reading time for dense content. For research-backed topics, mark demonstrative numbers as examples or verify them before rendering.

## 2. Prepare code and fonts

Create `index.html`, shared `common.js`, scene code and an audio synthesis script. Or create an HTML file for each scene. Define `window.DURATION` and `window.renderFrame(t)` on each entry page. Favor one global dispatcher when many short cuts share assets; use isolated pages for conflicting WebGL/SVG setups or parallel construction. In either case the frame function must be seekable. Fonts should be open-source, locally installed or otherwise reliably loadable, and their licenses should ship with the project when bundled. Confirm glyph coverage for the chosen language.

Install Python dependencies from `requirements.txt`; install Playwright Chromium (`python -m playwright install chromium`) or use a local Chrome/Edge binary; provide `ffmpeg` and `ffprobe` on PATH. When `.browsers` exists in the working directory, `scripts/render_frames.py` uses it automatically. On Windows, the script discovers Chrome or Edge if Playwright's managed browser is absent. `--executable` overrides discovery. Use an isolated Python environment. Set temporary-directory overrides only when the host environment requires them.

## 3. Preview before full render

For one global page:

```text
python scripts/render_frames.py project/index.html --frames TOTAL --fps FPS --preview preview.jpg
```

For each longer scene, use `--t0 START_SECONDS --frames SCENE_FRAMES` to inspect six frames. For isolated scene pages, omit `--t0`; their frame functions start locally at zero. Inspect the contact sheet at full size. Then inspect frames directly adjacent to each cut, plus the flash peak and the first readable frame. A six-frame sample cannot prove that no middle frame glitches exist.

The preview helper captures a timestamp twice and compares its JPEG bytes for a determinism smoke check. When it fails, inspect seeded randomness, mutable counters, pending fonts and asynchronous textures.

## 4. Render and make audio

Render a global page with `--output visual.mp4`. For isolated scene pages, render each to an MP4 using identical fps, dimensions, codec settings and pixel format. Join them with FFmpeg's concat demuxer and `-c copy`, then probe the joined file's frame count. If concat produces timestamp or frame-count errors, normalize the segments with the same encoding command, or render a single global page.

Use a Python score driven by the same scene boundary and hit indices. The bundled example `examples/being-and-void/score.py` demonstrates seeded plucks, pads, noise and stereo effects. Compose a new arrangement for each topic. Generate stereo PCM WAV at a declared sample rate. Listen at each cut and the final fade. Convert video plus WAV to a delivery MP4:

```text
ffmpeg -i visual.mp4 -i soundtrack.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -movflags +faststart final.mp4
```

If distribution size matters, use a separate two-pass H.264 copy with a chosen bitrate, then repeat every final check. Do not assume a 26 MB target is right for a different duration or scene complexity.

## 5. Verify and deliver

```text
python scripts/verify_video.py final.mp4 --width W --height H --fps FPS --frames TOTAL
python scripts/contact_sheet.py final.mp4 full_contact.jpg --interval 1
```

Watch `final.mp4` end to end with sound. Inspect the 1 fps contact sheet for missing scenes; inspect cut-adjacent frames because 1 fps can miss a single bad frame. Check no audio clipping, incorrect or missing hits, unreadable copy, unintended black frames, late font swaps, crop errors or abrupt tails. Deliver the final MP4, source, plan/manifest, contact sheets and a short verification report. Record any deliberate simplifications such as Canvas approximations of a requested 3D look.

## Recovery

| Symptom | First check | Recovery |
| --- | --- | --- |
| Chromium fails | Browser installation and executable path | Install Playwright Chromium or pass `--executable`; preserve SwiftShader flags for WebGL |
| Blank WebGL frame | Drawing buffer and render timing | Set `preserveDrawingBuffer: true`, render synchronously, then capture |
| Fonts shift | `document.fonts.ready`, explicit font load, glyph coverage | Bundle open font, load before capture, re-preview |
| Render too slow | `ctx.filter`, shadows, excessive path/particles | Pre-render static layers, cache geometry, reduce effects, keep intended composition |
| Hit drifts | Mixed seconds/frame arithmetic | Rebuild events from integer frame plan, regenerate audio and visual output |
| Concat has gaps | Segment fps/codec/timebase mismatch | Re-encode matching segments or use global dispatcher |
| Final fails checks | Probe the actual delivered MP4 | Fix source or encode, then re-run all delivery checks |
