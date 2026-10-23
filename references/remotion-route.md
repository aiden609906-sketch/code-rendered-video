# Optional Remotion + 3D route

Choose this when a topic benefits from a persistent 3D subject, spatial camera work and React-layer typography. For simpler vector or Canvas compositions, use the HTML/Playwright route in the main skill. A Remotion project is still a pure-code video when its imagery and soundtrack are rendered or synthesized in code and asset constraints are observed.

## Composition contract

- Pin the project dependency versions and record them with the source. Set composition width, height, fps and exact duration in integer frames. Keep one `plan.ts` (or equivalent) for scene boundaries, subtitle cues, beat events and transitions. Assert contiguous scenes and exact final frame count.
- Build each scene as a component driven by `useCurrentFrame()` and `useVideoConfig()`. Use `interpolate()` and `spring()` with explicit frame ranges. Avoid wall clock, `Math.random()`, uncontrolled timers and browser animation loops; use a seeded PRNG or precomputed deterministic values.
- For React Three Fiber, use `ThreeCanvas` from `@remotion/three` with explicit width and height. Animate from Remotion's frame, not R3F `useFrame()`. Treat text as HTML/React overlay when glyph coverage or subtitle legibility makes 3D text unreliable.
- Bundle fonts and wait for them and other asynchronous assets before rendering (`delayRender` / `continueRender` where appropriate). Keep sources and licenses with the project. Batch dense particles with instancing/points and test costly effects on the actual render machine.

## Preview, render and recovery

1. Preview all scenes in Remotion Studio at first, middle and last frames; also inspect cut-adjacent frames and the full subtitle track. Render short representative ranges before the full film. Do not feed a React composition to `scripts/render_frames.py`.
2. Render through Remotion's CLI or project script with the pinned project version. Select the WebGL backend after testing the target machine; do not assume a particular `--gl` setting or GPU is always best. Record the command and output settings. If fonts/objects flicker, resolve asset readiness and deterministic state first; reducing concurrency is a diagnostic/workaround, not the design fix.
3. If rendering fails late, render frame ranges or scenes separately with matching codec, resolution, fps and pixel format, then join and verify timestamps and frame count. The Python `verify_video.py` and `contact_sheet.py` can inspect the resulting MP4 independently of the renderer.
4. Synthesize and mux audio from the same integer-frame event map used by the composition. Review the delivered MP4 at normal speed and confirm facts and subtitle readability.

Official references: [ThreeCanvas](https://www.remotion.dev/docs/three-canvas), [WebGL render option](https://www.remotion.dev/docs/cli/render#--gl), [flickering diagnosis](https://www.remotion.dev/docs/flickering). Check current documentation before choosing CLI flags or packages.
