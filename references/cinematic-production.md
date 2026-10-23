# Cinematic production from code

Use when the subject benefits from photographed objects, spatial depth or restrained camera work. The bundled Three.js example is one art direction, not a compulsory visual style.

- Build a coherent subject with readable silhouette and physically meaningful construction: hollow vessels, real openings, connected spokes. Model details only where camera distance reveals them.
- Design wide, medium, detail and reverse shots before polishing shaders. Connect cuts through shape, direction and cause; reserve stillness for understanding.
- Use motivated key and rim light, negative fill and deliberate exposure. Procedural roughness and restrained surface variation should explain material, not obscure it.
- Use a color/depth render target for lens blur when appropriate; tune focus and edge artifacts at full resolution. Software rendering can make this expensive: simplify samples or use selective precomputed blur after inspecting the result.
- Keep captions off the subject. Check the closest crop, longest line and every camera transition; remove redundant giant text from object detail shots.
- Explicitly load every font face before first capture. Seek A → B → A across scenes to catch mutable material, light and visibility state. Test on the selected backend; do not compare pixel hashes between different GPUs as if identical output were guaranteed.
- Default to SwiftShader for portability. On Windows, `--angle d3d11` can be faster; first inspect the actual renderer with the example GPU probe, then run QA. Preserve the software fallback. Render speed and visual quality depend on hardware and scene cost.
- Listen to the score and watch the final delivery at normal speed. If the agent cannot perform that review, mark it as outstanding; sampled frames and signal measurements do not establish aesthetic approval.

The example has 23 shots over 90 seconds. Its cut density, celadon palette, Chinese copy and pentatonic score belong to its topic. Reuse the scene contract, camera planning, font readiness, cross-scene seek tests and delivery checks.
