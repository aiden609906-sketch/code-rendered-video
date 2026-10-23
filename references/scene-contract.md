# Deterministic scene contract

Each HTML entry exposes `window.DURATION` in seconds and `window.renderFrame(t)`. In a single-page edit, `t` is global film time; the dispatcher finds the active segment using an integer frame table. In a per-segment edit, `t` is local segment time. For segment reuse, apply `sceneTime = t0 + localTime * speed` exactly once. Keep the audio and cut schedule on the same integer frame table.

Draw from absolute time, fixed data and a fixed seed. Recreate particle positions from `mulberry32(seed)` at each call or use a fixed precomputed array; do not step a simulation forward. On every call reset Canvas state, transforms, alpha, filters and line dashes. Wait for `document.fonts.ready` and explicit `document.fonts.load(...)` before capturing. If WebGL is used, seek animation from absolute time and render once within `renderFrame`; enable `preserveDrawingBuffer: true`.

For an impact-enabled segment, during local time `u`: white flash alpha `0.85 * (1-u/0.12)` while `u < 0.12`; scale `1.13 → 1` with outCubic over 0.32 s; shake at most 14 px decaying over 0.16 s; then push toward 1.05 over the remainder of the segment. A capsule number and style name belong at top left when a style showcase uses them; they are not required for unrelated topics.

When using multiple HTML pages, pass `?seg=1&t0=&speed=&dur=` and let the scene map local time to its source animation. When using one HTML page, the scene dispatcher can make that mapping directly.

Minimal global dispatcher:

```js
const FPS = 30;
const shots = [
  {start: 0, end: 120, draw: drawOpening},
  {start: 120, end: 1800, draw: drawMain}
];
window.DURATION = 1800 / FPS;
window.renderFrame = t => {
  const frame = Math.min(1799, Math.max(0, Math.floor(t * FPS + 1e-6)));
  const shot = shots.find(s => frame >= s.start && frame < s.end);
  const local = (frame - shot.start) / FPS;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalAlpha = 1;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  shot.draw(local);
};
```

Avoid per-frame `ctx.filter` blur and large `shadowBlur` with software rendering. Pre-render costly blurred layers and crossfade them. Repeated captures of the same timestamp should have identical pixels; use hashes on selected frames to test that property.
