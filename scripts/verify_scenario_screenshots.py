#!/usr/bin/env python3
"""Stdlib verification for the bilingual, action-annotated Control tutorials."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "select-connector", "run-test", "record-selection", "field-mapping",
    "add-static-field", "deploy-readiness", "stream-actions",
    "dashboard-triage", "source-api-error", "saved-draft",
}
IMG_PATTERN = re.compile(
    r"!\[[^\]]+\]\((/images/screenshots/annotated/([a-z-]+)\.webp)\)"
    r"\n\n\*(그림|Figure) (\d+)\.",
)
ALL_IMAGES = re.compile(r"!\[[^\]]*\]\((/images/screenshots/annotated/[^)]+)\)")
SITE_LINK = re.compile(r"\]\((/[^)#]+)(?:#[^)]*)?\)")

def verify() -> None:
    errors: list[str] = []
    total_captions = 0
    nav = json.loads((ROOT / "docs.json").read_text(encoding="utf-8"))
    for lang in nav["navigation"]["languages"]:
        for group in lang["groups"]:
            for page in group["pages"]:
                if not (ROOT / (page + ".mdx")).is_file():
                    errors.append("Broken nav: " + page)
        prefix = "ko/use-cases/" if lang["language"] == "ko" else "use-cases/"
        if prefix + "screen-walkthrough" not in [
            x for group in lang["groups"] for x in group["pages"]
        ]:
            errors.append("Missing visual guide in navigation: " + lang["language"])

    en_names = {p.name for p in (ROOT / "use-cases").glob("*.mdx")}
    ko_names = {p.name for p in (ROOT / "ko/use-cases").glob("*.mdx")}
    if en_names != ko_names:
        errors.append(f"EN/KO page mismatch: {en_names ^ ko_names}")

    for folder in ("use-cases", "ko/use-cases"):
        for page in (ROOT / folder).glob("*.mdx"):
            text = page.read_text(encoding="utf-8")
            if not text.startswith("---\n") or text.count(chr(96)*3) % 2:
                errors.append("Broken MDX/frontmatter: " + str(page))
            if "## Additional UI walkthrough captures" in text or "## 추가 화면 예시" in text:
                errors.append("Old detached gallery: " + str(page))
            if "/images/screenshots/verified/" in text:
                errors.append("Unannotated image: " + str(page))
            images = ALL_IMAGES.findall(text)
            matches = IMG_PATTERN.findall(text)
            if len(images) != len(matches):
                errors.append("Missing adjacent figure captions: " + str(page))
            ordered = [int(m[3]) for m in matches]
            if ordered != list(range(1, len(matches) + 1)):
                errors.append("Out-of-order figure numbering: " + str(page))
            for link in SITE_LINK.findall(text):
                rel = link.removeprefix("/")
                if not ((ROOT / rel).is_file() or (ROOT / (rel + ".mdx")).is_file()):
                    errors.append(f"Broken internal link: {page}: {link}")
            total_captions += len(matches)

    assets = {p.stem for p in (ROOT / "images/screenshots/annotated").glob("*.webp")}
    if assets != EXPECTED:
        errors.append("Unexpected annotated asset inventory: " + str(assets ^ EXPECTED))
    for img in (ROOT / "images/screenshots/annotated").glob("*.webp"):
        data = img.read_bytes()
        if len(data) < 5000 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
            errors.append("Corrupt WEBP: " + str(img))

    print(f"EN_PAGES={len(en_names)} KO_PAGES={len(ko_names)}")
    print(f"ANNOTATED_ASSETS={len(assets)} FIGURES_WITH_CAPTIONS={total_captions}")
    print(f"ISSUES={len(errors)}")
    for err in errors[:50]:
        print("ERROR:", err)
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    verify()
