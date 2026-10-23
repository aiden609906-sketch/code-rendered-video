---
name: code-rendered-video
description: Use when a user wants a topic turned into a polished, beat-synced video rendered from code, with synthesized audio, frame-level QA and a verified MP4. Supports fast visual showcases and longer, protagonist-led explainers. A topic alone is sufficient; use explicit duration, format, language or brand details when provided.
---

# Code-rendered video

Turn a topic into a finished video, not merely a prompt or storyboard. The user only needs to supply a topic. Infer a suitable audience, message, language, visual motif, runtime and music feel; state these assumptions briefly and proceed. Ask only when a missing fact would make the video misleading (for example, an exact product claim or required brand asset). Honor explicit constraints over defaults.

Typical invocation: `$code-rendered-video 主题：城市夜跑。`

## Default contract

- Input: topic. Optional: audience, takeaway, facts/sources, language, duration, aspect ratio, brand, call to action, reference style, audio preferences.
- Default output: 1920×1080, 30 fps, H.264/yuv420p video and AAC audio; a concise production plan, source project, six-frame contact sheet per scene, final MP4 and verification report.
- Default length: choose 30–60 seconds for a visual showcase; allow roughly 60–180 seconds for an explainer when the script warrants it. Choose the shortest duration that keeps the argument and text legible. Use 120 BPM only when no tempo is given. Put major cuts and hits on a beat grid without forcing every scene to the same length.
- Do not use generated video, imagery, music, speech or stock footage when the request calls for pure code. Render visuals with HTML/Canvas/SVG/WebGL; synthesize audio with code. Use only licensed or open-source fonts and record their provenance. A user-supplied asset is permitted only when the user allows it.

## Workflow

1. Choose a format from the topic: a rhythmic style showcase, a protagonist-led explainer, or a chaptered catalog. Create a compact topic-specific plan using [the plan template](references/plan-template.md). If a reference video is supplied, probe it and review a time-sampled contact sheet before designing; record its duration, shot density, camera movement, visual depth, subtitle cadence and sound structure. Match the *level of production detail* that the user points to while making original scenes and checking facts. For an explainer, set an early hook, one recurring visual subject, a clear question-to-answer arc and a closing payoff. Pair every script beat with a visible action; use [narrative explainer guidance](references/narrative-explainers.md). For a showcase, prioritize contrast between styles and an exact cut map. Verify material facts against primary sources before putting them on screen. Avoid copying the Opus 5.5 wording, 11-style sequence or 61-second runtime unless requested.
2. Choose the renderer according to the visual problem. The default Canvas/SVG/WebGL route uses one HTML page with a global `renderFrame(t)` and scene dispatcher, or one page per segment with local `renderFrame(t)`. Each page exposes `window.DURATION`; each frame depends only on `t`, fixed assets and a fixed seed. Use no CSS transitions or animations, `requestAnimationFrame`, wall clock, unseeded randomness or asynchronous content that can change between captures. Use [scene contract](references/scene-contract.md). For a genuine 3D protagonist with React-layer subtitles, use the optional [Remotion route](references/remotion-route.md); it has its own frame-driven renderer and preview commands.
3. Preview six representative frames per scene with the appropriate renderer and make contact sheets; inspect them at full size. Fix clipping, unreadable text, inconsistent margins, weak contrast, awkward pauses and incorrect first impact frames before full rendering. Check the first and last frame of each scene and frames around every cut. If subtitles carry the story, read the full film at normal playback speed, check line duration and ensure the subject remains visible. For a supplied reference, compare a contact sheet of the work against it: long static diagrams, empty first frames or a much shorter script should trigger revision before full render.
4. On the HTML route, render each scene with Playwright Chromium using `renderFrame(i/fps)`, then CDP `Page.captureScreenshot` as JPEG quality 95, piped to FFmpeg `image2pipe` and `libx264 -crf 16 -pix_fmt yuv420p`. If using WebGL, launch Chromium with `--use-angle=swiftshader --enable-webgl --ignore-gpu-blocklist` and create the renderer with `preserveDrawingBuffer: true`. On the Remotion route, use its own render pipeline; never pass a React composition to the HTML capture script. Render the exact integer frame allocation in the plan.
5. Synthesize the audio on the same beat and frame timeline; place transients deliberately at cuts, control peak level and leave the final tail clean. Use the bundled cinematic example score as an architectural example; compose a new topic-specific arrangement. Listen and revise. Mux AAC and run FFprobe to check dimensions, frame count, duration and streams. A final distribution encode may use two-pass compression if size matters; inspect that encode again.
6. Review the full MP4 at normal speed with sound. Iterate at least once if any scene fails a quality gate. If a scene is too costly or unstable, replace the technique with simpler code-rendered geometry while preserving its intended message and beat placement. Report unresolved limitations plainly; never claim identical quality across arbitrary topics without review.

## Quality gates

| Gate | Required evidence |
| --- | --- |
| Plan | One clear thesis, justified scene order, exact start/end frames; hook and payoff for explainers; no unsupported factual claim |
| Visual | Contact sheets reviewed; type readable at normal playback; no clipping, blank frames or accidental layout jumps |
| Timing | Cuts and audio transients share frame indices; total allocated frames equal target exactly |
| Determinism | Repeated capture of a sampled timestamp is visually identical; no uncontrolled render state |
| Audio | No audible clipping, abrupt truncation or accidental silence; music supports narration/text cadence |
| Story and text | If subtitle-led: each line has adequate viewing time and a meaningful on-screen action; recurring subject stays recognizable; hook and ending resolve the same question |
| Reference fit | When a reference is supplied, contact-sheet comparison shows comparable narrative coverage, scene variety and shot density; intentional deviations are documented |
| Delivery | FFprobe confirms target width, height, fps, exact video frame count, H.264 and AAC; MP4 watched end to end |

## Starter and use

Read [scene contract](references/scene-contract.md), [narrative explainers](references/narrative-explainers.md), [cinematic production](references/cinematic-production.md) and [production runbook](references/production-runbook.md) as needed. The optional [Remotion route](references/remotion-route.md) requires its own dependencies. `scripts/render_frames.py`, `scripts/verify_video.py` and `scripts/contact_sheet.py` support HTML capture and independent checks. Install `requirements.txt`, Playwright Chromium and FFmpeg/FFprobe. A complete, topic-specific Three.js film and synthesized score are included under `examples/being-and-void/`; inspect its README before adapting it. Raw user conversations and private reference videos are not distributed.

## Reuse boundary

Reusable: deterministic frame timing, seeded effects, beat/frame accounting, renderer-specific capture, code synthesis methods, contact-sheet review, factual-claim checks and verification. Topic-specific: format, message, protagonist or visual metaphor, claims, palette, fonts, sequence, copy, soundtrack and hand-polished motion. Examples supply story structures and art directions, not universal timings, palettes or factual claims. Consistent quality is a target established through review and revision; it cannot be guaranteed from an arbitrary topic without iteration.
