# Narrative explainer route

Use this route when a topic needs an explanation, causal journey or question answered over time. Treat numbers, prescriptions and topic claims in supplied prompts as unverified source material.

## Build the story

1. Form one precise viewer question and one takeaway. Open with a concrete hook quickly, ideally in the first few seconds. Establish the subject in the first readable frame; use a dark or delayed reveal only when it serves the hook.
2. Pick a recurring visual subject that can change state: a photon traveling, a real QR code being decomposed, a character choosing between paths, or a recurring card/object linking chapters. This is a continuity device, not a mandatory cartoon mascot.
3. Outline a causal arc: hook → what the viewer needs to know → discovery or mechanism → consequence → payoff that answers the opening question. For a catalog, use a repeated chapter grammar and a final synthesis. Give complex ideas a visual pause.
4. Write scene rows as `frame range | spoken/on-screen line | subject state | visible action | camera | audio event | claim/source | QA risk`. A line change should normally coincide with a meaningful visual change. Deliberate stillness is fine when it helps understanding; avoid static text replacement that leaves the viewer with nothing new to inspect.
5. Reuse visual landmarks across cuts so the viewer understands location and causality. Choose transitions from story logic: follow the subject, match shape/direction, or cut on a cause-and-effect event. Simple cuts are valid.

If a reference film is provided, measure its runtime and sample it across the timeline. Count meaningful changes within scenes, not just hard cuts. A short plan with a handful of static cards does not satisfy a long cinematic reference even when the colors and subtitles resemble it. Build a scene-by-scene comparison before rendering: subject state, camera scale, background depth, text cadence, sound hit and payoff. Borrow the design logic; create original frames and independently validate claims.

## Subtitles as narration, when chosen

Use this only for a silent explainer or when the user requests text-led narration. If there is a spoken track, captions should follow the actual voice and should not duplicate every visual label. Draft the full script before timing shots. At 30 fps, a two-to-three-second line is a starting point, not a limit; count characters and test at normal viewing speed. Keep most lines to one or two lines, with enough contrast against their actual background. Highlight only meaningful words. Move or reshape the text block when the subject occupies its default region. Use local font files with Chinese glyph coverage when needed, and confirm their licenses. Preview the longest line, the fastest cut and a scene where the subtitle overlaps complex imagery.

## Claim and depiction ledger

Before animating, list every numeric, historical, health, scientific, product or financial claim. For each one record the exact wording, primary source URL or document, retrieval date, calculation and uncertainty. Recompute displayed ratios, distances and running counters from documented input values. Mark estimates and diagrams as simplified when they are. Do not inherit factual assertions from the prompt examples without verification. A code-rendered object that claims a real-world function must function: a displayed QR code that is said to be scannable must be generated from actual content and scan-tested; a map presented as geographically accurate needs suitable geodata and attribution. If credible support cannot be found, revise or omit the claim rather than invent a source.

## Visual and pacing checks

- Check subject silhouette, text contrast, hierarchy, safe margins, cuts, and camera path at full resolution. Brightness, bloom, rim light and 3D materials are style choices; tune them to the concept and avoid washed-out text.
- Motion must remain seekable and tied to frame time. Long particle fields should use batching/instancing. Cache expensive static layers. Choose smooth camera paths where they help orientation; do not add movement solely to meet a rule.
- Review the full film with audio. Pause at the hook, the explanatory turn and the final answer: the same question should be traceable through all three.
- If the build or duration is too expensive, shorten or simplify scenes while keeping the causal explanation and verified claims intact.

## Example routing

- “二维码会被用完吗？”: likely a protagonist-led explainer; generate a real QR if scan ability is asserted, verify capacity and combinatorics, and derive numbers in code. Do not copy the example's constants blindly.
- “展示 11 种品牌设计风格”: likely a rhythmic showcase; a recurring protagonist and subtitle-led narration are optional, while contrast, cut rhythm and contact sheets matter most.
