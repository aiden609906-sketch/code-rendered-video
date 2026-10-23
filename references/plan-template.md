# Topic-specific production plan

Keep this to one page before implementation; update it when edits change the cut.

```text
Topic:
Format (showcase / narrative explainer / chaptered catalog):
Audience / single takeaway:
Assumptions (language, format, duration, tempo, brand):
Source and licensing notes:
Opening hook / recurring subject and its states / final payoff (if narrative):
Script mode (subtitles as narration / voice + captions / music + labels):
Facts to verify / sources / calculations and uncertainty:
Visual grammar (type, palette, margins, motifs, transition rule):
Audio grammar (tempo, instruments, accent pattern, peak target):
Ending / call to action:
Renderer (HTML + Playwright / Remotion + optional 3D) and why:

Shot | start frame | end frame (exclusive) | narration/subtitle or label | subject state + visible action | camera | audio hit | claim/source | QA risk
...

Total frames = sum(end-start). Every frame is assigned once. At 30 fps,
a 60-second film has 1800 frames; at 120 BPM one beat is 15 frames.
```

Use a manifest next to the scene files. Paths are relative to the manifest directory. `id` is a stable filename stem. `start_frame` and `frames` are integers. `scene` is an HTML path, or use the same entry page for a single-page dispatcher. `t0` and `speed` are optional scene-time mapping parameters. `impact` marks a code-rendered hit overlay. `hit` marks an audio accent at the first frame. Implement these fields in the project renderer and audio script; this is a handoff schema, not a bundled universal renderer.

```json
{
  "title": "Example topic",
  "width": 1920,
  "height": 1080,
  "fps": 30,
  "bpm": 120,
  "sample_rate": 48000,
  "total_frames": 1800,
  "segments": [
    {"id": "opening", "scene": "index.html", "start_frame": 0, "frames": 120, "hit": true},
    {"id": "idea_01", "scene": "index.html", "start_frame": 120, "frames": 1680, "t0": 0, "speed": 1, "impact": true, "hit": true}
  ]
}
```

This JSON illustrates the schema, not a recommended two-scene edit. Pick scene lengths and count for the topic. Place accents at `start_frame` or beat offsets that match the visual event. Avoid a scene duration that ends between readable text phrases.

For a Remotion project, express the same integer boundaries and subtitle/audio event indices in `plan.ts` or an equivalent single source of truth. Do not force its React composition into this HTML manifest. For an explainer, keep a separate claim ledger with source URLs and calculated values; for a pure visual showcase, omit empty story fields rather than inventing a protagonist.
