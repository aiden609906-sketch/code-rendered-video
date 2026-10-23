# Code Rendered Video

**输入一个主题，让编程 agent 制作经过检查的代码视频。**

A portable agent skill for topic-driven, code-rendered films: deterministic HTML/Canvas/SVG/Three.js visuals, Python-synthesized audio, beat/frame timing, contact-sheet review and verified MP4 delivery. No image, video or music generation model is required.

![有无相生 · 代码渲染示例](docs/poster.jpg)

## 安装与使用 / Install

Clone this repository into your agent's skill directory as `code-rendered-video`. For Codex, the usual location is `~/.codex/skills/code-rendered-video`. Restart or refresh the agent's skill discovery if needed. Other agents that support `SKILL.md` can use the same folder; otherwise ask the agent to read `SKILL.md` explicitly.

```text
$code-rendered-video 主题：有无相生的道理
```

Only a topic is required. Optional inputs include language, audience, duration, aspect ratio, brand, reference video and soundtrack preference. The agent plans and writes topic-specific scenes; this is not a fixed renderer that replaces a title in a template.

## Runtime prerequisites

- Python 3.12+ recommended; install `requirements.txt` in a virtual environment.
- Install Chromium: `python -m playwright install chromium`.
- FFmpeg and FFprobe available on PATH.
- For the bundled film, use its pinned `examples/being-and-void/requirements.txt` in a separate environment. Browser installation may require network access and Linux system packages.

The default renderer is Playwright + software WebGL. Windows native GPU rendering is optional and must pass its own readiness and determinism checks. Remotion is an optional, separately installed route.

## What is included

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Topic-only input, production process, quality gates and reuse boundaries |
| `references/` | Planning template, scene contract, narrative and cinematic direction, failure recovery |
| `scripts/` | Deterministic browser capture, contact sheets and MP4 verification |
| `examples/being-and-void/` | Complete 90-second Chinese Three.js film, procedural materials, cameras and synthesized score |
| `docs/contact-sheet.jpg` | Time-sampled frames from a previous example render |

The example README explains how to preview, render and verify the film. Its fonts and Three.js are bundled with their licenses. Rendered MP4/WAV files are generated locally and are excluded from Git.

## Quality and limitations

Reusable: frame accounting, seeded effects, capture pipeline, audio synthesis techniques, font readiness, contact-sheet review, cross-scene seek tests and encoding checks.

Topic-specific: thesis, facts, script, visual metaphor, geometry, materials, camera paths, pacing, palette and musical arrangement. New topics require new creative work and iteration. Equal quality from every arbitrary topic is not guaranteed. Hardware, font rasterization and browser versions can affect pixels and render time.

Default delivery is 1920×1080 / 30 fps / H.264 + AAC, with source, plan, previews and verification report. Automated checks do not replace watching and listening; any unperformed review must be reported honestly. The included preview is evidence for that example only, not a benchmark for all future topics or platforms.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Improvements backed by a reproducible scene, failure case or before/after preview are welcome.

## License

Project-authored code, skill text and example artwork: [MIT](LICENSE). Bundled dependencies retain their own licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). No endorsement or affiliation with OpenAI, Anthropic or the Three.js/font projects is implied.
