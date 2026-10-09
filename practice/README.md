# practice

A tiny CLI to log coding-practice sessions (LeetCode, etc.) — for tracking your own real practice, honestly.

## Usage

```bash
# Log a solve
python leetcode_log.py add "Two Sum" --difficulty easy \
  --topics "arrays,hashmap" --notes "O(n) single pass with hashmap"

# List history
python leetcode_log.py list
python leetcode_log.py list --recent 10

# Totals, top topics, current streak
python leetcode_log.py stats
```

Data is stored in `log.json` next to the script. Stdlib only.
