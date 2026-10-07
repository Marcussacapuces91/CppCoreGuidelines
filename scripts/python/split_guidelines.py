#!/usr/bin/env python3
from pathlib import Path
import re
import unicodedata

src = Path("CppCoreGuidelines.md")
out_dir = Path("guidelines")
out_dir.mkdir(exist_ok=True)

# remove previous generated files if you want a clean run
for file in out_dir.glob("*.md"):
    file.unlink()

lines = src.read_text(encoding="utf-8").splitlines()
header_re = re.compile(r"^#\s+(.*)$")

sections = []
current_title = None
current_lines = []

def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9\s-]", "", normalized).strip().lower()
    normalized = re.sub(r"[\s-]+", "-", normalized)
    return normalized or "section"

for line in lines:
    match = header_re.match(line)
    if match:
        if current_title is not None and current_lines:
            sections.append((current_title, current_lines))
        current_title = match.group(1).strip()
        current_lines = [line]
    else:
        if current_title is not None:
            current_lines.append(line)

if current_title is not None and current_lines:
    sections.append((current_title, current_lines))

for index, (title, body) in enumerate(sections, start=1):
    slug = slugify(title)
    filename = out_dir / f"{index:03d}-{slug}.md"
    content = "\n".join(body).rstrip() + "\n"
    filename.write_text(content, encoding="utf-8")

print(f"Generated {len(sections)} files in {out_dir}")
