#!/usr/bin/env python3
"""Log coding-practice sessions (LeetCode, etc.) — tiny CLI, JSON storage.

Usage:
    python leetcode_log.py add "Two Sum" --difficulty easy --topics "arrays,hashmap" --notes "O(n) with hashmap"
    python leetcode_log.py list
    python leetcode_log.py stats

Data lives in practice/log.json next to this script.
"""

import argparse
import json
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

STORE = Path(__file__).resolve().parent / "log.json"


def load() -> list:
    if STORE.exists():
        return json.loads(STORE.read_text())
    return []


def save(entries: list) -> None:
    STORE.write_text(json.dumps(entries, indent=2) + "\n")


def cmd_add(args) -> None:
    entries = load()
    entries.append(
        {
            "date": date.today().isoformat(),
            "problem": args.problem,
            "difficulty": args.difficulty,
            "topics": [t.strip() for t in args.topics.split(",") if t.strip()],
            "notes": args.notes or "",
        }
    )
    save(entries)
    print(f"Logged: {args.problem} ({args.difficulty})")


def cmd_list(args) -> None:
    entries = load()
    if args.recent:
        entries = entries[-args.recent :]
    for e in entries:
        topics = ", ".join(e["topics"])
        print(f"{e['date']}  [{e['difficulty']:6}] {e['problem']}  ({topics})")
        if e["notes"]:
            print(f"           {e['notes']}")


def cmd_stats(_args) -> None:
    entries = load()
    if not entries:
        print("No entries yet.")
        return
    by_diff = Counter(e["difficulty"] for e in entries)
    by_topic = Counter(t for e in entries for t in e["topics"])
    print(f"Total solved: {len(entries)}")
    print("By difficulty:", dict(by_diff))
    print("Top topics:", dict(by_topic.most_common(5)))

    # Current streak (consecutive days with at least one solve, ending today/yesterday).
    days = sorted({e["date"] for e in entries}, reverse=True)
    day_set = set(days)
    cursor = date.today()
    if cursor.isoformat() not in day_set:
        cursor -= timedelta(days=1)
    streak = 0
    while cursor.isoformat() in day_set:
        streak += 1
        cursor -= timedelta(days=1)
    print(f"Current streak: {streak} day(s)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Log coding-practice sessions.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="Log a solved problem")
    p_add.add_argument("problem", help="Problem name")
    p_add.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="medium")
    p_add.add_argument("--topics", default="", help="Comma-separated topics")
    p_add.add_argument("--notes", default="", help="What you learned / approach")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List logged problems")
    p_list.add_argument("--recent", type=int, default=0, help="Show only the last N entries")
    p_list.set_defaults(func=cmd_list)

    p_stats = sub.add_parser("stats", help="Show totals and streak")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
