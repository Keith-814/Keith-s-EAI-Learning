"""Small CI checks for the generated project site."""

from pathlib import Path
from urllib.parse import urlparse
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
BASEURL = "/Keith-s-EAI-Learning"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


if not SITE.is_dir():
    fail("_site/ does not exist; run Jekyll first")

html_files = list(SITE.rglob("*.html"))
if not html_files:
    fail("no generated HTML files found")

errors = []
for html in html_files:
    text = html.read_text(encoding="utf-8", errors="replace")
    for value in re.findall(r"(?:href|src)=\"([^\"]+)\"", text):
        parsed = urlparse(value)
        if parsed.scheme or value.startswith("//"):
            continue
        path = parsed.path
        if not path.startswith(BASEURL):
            continue
        local = path[len(BASEURL):].lstrip("/")
        candidate = SITE / local
        if candidate.is_dir():
            candidate = candidate / "index.html"
        if not candidate.exists():
            errors.append(f"{html.relative_to(SITE)} -> {value}")

for required in [
    "index.html",
    "research/index.html",
    "timeline/index.html",
    "VLA-Survey/index.html",
    "World-Models-Survey/index.html",
    "style.css",
]:
    if not (SITE / required).exists():
        errors.append(f"missing generated file: {required}")

if errors:
    for error in errors[:40]:
        print(error, file=sys.stderr)
    if len(errors) > 40:
        print(f"... and {len(errors) - 40} more", file=sys.stderr)
    raise SystemExit(1)

print(f"Checked {len(html_files)} HTML pages and required assets.")
