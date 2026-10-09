# digest-gen

Generates the daily Engineering Digest markdown from a JSON entries file and keeps the repo's README index up to date. This is the script the daily digest job actually runs.

## Usage

```bash
python generate_digest.py entries-2026-10-09.json \
  --repo /path/to/engineering-digest \
  --highlights "Netflix at scale; GC tuning for Spring Boot"
```

## Entries file format

```json
{
  "date": "2026-10-09",
  "theme": "production reality",
  "intro": "Six reads worth your time today.",
  "entries": [
    {
      "section": "Distributed Systems",
      "title": "Building Service Topology at Scale",
      "author": "Netflix Tech Blog",
      "url": "https://example.com/article",
      "summary": "Why it matters, in your own words."
    }
  ]
}
```

Writes `digests/<date>.md` and inserts (or replaces) the date's row in the README index table. Stdlib only.
