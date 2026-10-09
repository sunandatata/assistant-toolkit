#!/usr/bin/env python3
"""Generate a daily Engineering Digest markdown file from a JSON entries file.

Usage:
    python generate_digest.py entries-2026-10-09.json --repo /path/to/engineering-digest

The entries file looks like:
    {
      "date": "2026-10-09",
      "theme": "production reality",
      "intro": "Six reads worth your time today.",
      "entries": [
        {
          "section": "Distributed Systems",
          "title": "Building Service Topology at Scale",
          "author": "Netflix Tech Blog",
          "url": "https://...",
          "summary": "Why it matters, in your own words."
        }
      ]
    }

The script writes digests/<date>.md and updates the README index table.
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

FOOTER = "\n---\n*Curated by Muse, an AI assistant. Summaries are original; all linked content belongs to its authors.*\n"


def render_digest(data: dict) -> str:
    lines = [f"# Engineering Digest — {data['date']}", ""]
    theme = data.get("theme")
    intro = data.get("intro", "Reads worth your time today.")
    lines.append(f"{intro} The theme of the day: **{theme}**." if theme else intro)
    lines.append("")

    current_section = None
    for i, e in enumerate(data["entries"], 1):
        section = e.get("section", "General")
        if section != current_section:
            lines += [f"## {section}", ""]
            current_section = section
        byline = f" — {e['author']}" if e.get("author") else ""
        lines += [
            f"### {i}. {e['title']}{byline}",
            e["url"],
            "",
            e["summary"],
            "",
        ]
    lines.append(FOOTER.strip())
    return "\n".join(lines) + "\n"


def update_readme_index(repo: Path, digest_date: str, highlights: str) -> None:
    readme = repo / "README.md"
    text = readme.read_text()
    row = f"| [{digest_date}](digests/{digest_date}.md) | {highlights} |"
    if digest_date in text:
        # Replace the existing row for this date.
        text = re.sub(
            rf"^\| \[{re.escape(digest_date)}\].*$",
            row,
            text,
            flags=re.MULTILINE,
        )
    else:
        # Insert after the table header separator line.
        text = text.replace(
            "|------|-----------|",
            "|------|-----------|\n" + row,
            1,
        )
    readme.write_text(text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily engineering digest.")
    parser.add_argument("entries", help="JSON file with the day's entries")
    parser.add_argument("--repo", required=True, help="Path to the engineering-digest repo")
    parser.add_argument(
        "--highlights",
        default="",
        help="Short highlight text for the README index row",
    )
    args = parser.parse_args()

    data = json.loads(Path(args.entries).read_text())
    digest_date = data.get("date", date.today().isoformat())
    data["date"] = digest_date

    repo = Path(args.repo)
    digests_dir = repo / "digests"
    digests_dir.mkdir(parents=True, exist_ok=True)

    out = digests_dir / f"{digest_date}.md"
    out.write_text(render_digest(data))
    update_readme_index(repo, digest_date, args.highlights or data.get("theme", ""))

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
