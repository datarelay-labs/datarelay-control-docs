# Annotated screenshot evidence

The numbered WebP images in this directory are created deterministically by `scripts/annotate_scenario_screenshots.py` from original PNGs in `images/screenshots/verified/`.

- **Provenance:** historical Control Playwright/UX test screenshots retained in product snapshot `f7ae7b35d602a5e2cae141297ecdda8154f47172` (see `images/screenshots/verified/README.md`).
- **Edits:** lossless UI content crop, rectangular highlight outlines, numbered circles, and action labels. No controls, application text or example data were invented or synthesized.
- **Version caveat:** some images show a **historical six-step Wizard**; the current documented flow is **Connect → Sample & Record Selection → Destinations → Route Processing → Deploy**. Captions always describe the *captured* UI action; the current deployed UI takes precedence.
- **Scope:** images demonstrate screen interactions only. They do not prove real API access, successful delivery, effective Route policy, a live Webhook/Syslog destination, a successful Quarantine/Replay, or latest product UX acceptance.
- **Usage:** images appear adjacent to applicable scenario steps with numbered English/Korean captions. Do not restore the prior end-of-page screenshot gallery or reuse an unrelated image as evidence of a feature.

To regenerate: `python3 scripts/annotate_scenario_screenshots.py` (requires Pillow). Inspect the output visually and update annotations if source screenshots change.
