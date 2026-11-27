---
title: Replacing 900-line agent manuals and cron loops with an 80-byte cursor
description: Moving cron polling, spam filtering, and drift checks out of LLM prompts into small Python scripts cut quota burn and stale docs.
date: 2026-11-28
slug: cutting-agent-prose-and-polling-noise
---
Moving cron polling, spam filtering, and drift checks out of language-model prompts into small Python scripts cut our quota burn and stopped stale docs.

My earliest setup tried to buy reliability with longer instructions.
At its peak, one workspace carried a 26-skill prompt library and nearly 1,000 lines of operating prose.
Four separate markdown files repeated the same rate limits, resume rules, and channel caps.

Both habits failed fast.
Changing one number in code left three prose documents quietly stating the old rule.
Scheduled jobs also woke a model on a fixed timer when nothing had arrived.
Most runs burned quota reading newsletters, social digests, and "Thank you for applying" receipts while real human replies sat buried.

That failure matches [our conductor review](/p/enforced-production-process.html), [rigout's error-flag fix](/p/mcp-missing-error-flag.html), and [DocQA's bot-wall guard](/p/docqa-bot-check-and-citations.html).
A language model makes a poor cron daemon, spam filter, and state index.

## 1. Drift checks that never block live work

Updating five documentation files in the middle of an urgent fix wastes context and breaks focus.
Leaving them unchecked creates the opposite trap: the next session reads stale prose as current law.

We split the two jobs.
Canonical numbers live once in JSON or Python (`cadence_state.json`, `master.json`, `boards.txt`).
Shared markdown files hold short `<!-- LAIR-SYNC:START:caps -->` blocks instead of hand-edited tables.

A standard-library script (`lair_sync.py`) checks modification times and content invariants across six dependency chains, then serves `/state.json` locally:

```bash
python -c "
import time, subprocess, sys
t0 = time.perf_counter()
subprocess.run([sys.executable, '_positioning/tools/lair_sync.py', '--json'],
                check=True, stdout=subprocess.DEVNULL)
print(f'{(time.perf_counter() - t0) * 1000:.1f} ms')
"
```

The full snapshot finishes in about 45 ms and spends zero model tokens.
When `boards.txt` grew from 75 to 349 employer boards during a live run, `/state.json` flagged `DRIFT` without stopping the worker.
Running `lair_sync.py --sync` afterward updated every linked file in one pass.

## 2. Memory under 4 KB

Long transcripts tempt you to feed yesterday's chat back into today's prompt.
Cost climbs, and old mistakes return.

Outward writing instead keeps a JSON file under 4 KB with two short lists: `what_gained` and `never_repeat`.
When a concise webhook post brought a paying agency lead inbound, that pattern entered `what_gained`.
When an overused opener ("Most workflows break...") turned stale, a regex in `guard.py` blocked it for good.
Once a mistake becomes a test, the prompt stays short.

## 3. A 24/7 wakeup trigger at zero idle tokens

Fixed 15-minute cron runs waste quota on quiet nights and still lag when someone writes.
Enabling all X and Reddit emails makes things worse if digests flood the inbox.

Two small changes solved it:

1. In Reddit and X settings, we turned digests and marketing off and kept email alerts only for direct messages, chats, replies, and mentions.
2. Inside the local dispatcher (`dispatch.py`), `inbox_watch.py` polls Gmail's `users.history.list` endpoint every 60 seconds with a saved `startHistoryId` cursor.

On an empty minute, Gmail returns the current `historyId` in about 80 bytes and zero model tokens.
When a new message lands in `INBOX`, Python rules read only its headers and snippet:

- Promotions, forums, newsletters, social digests, and standard ATS receipts drop at the door.
- Four classes pass: X messages or replies, Reddit chats or replies, recruiter interview or screening links, and known human contacts.

A matching signal sends a two-line Telegram alert right away.
It wakes an idle agent at most once every 20 minutes (`<= 3` wakeups per hour).
Eleven unit tests in `test_board.py` and `test_inbox_and_sync.py` verify these filters and cooldowns in `0.04s`.

## What changed

The workspace runs quieter now.
Small scripts watch the clock, filter the inbox, and track which files drifted.
The model wakes only when there is code to ship or a person waiting on the other side.

If your team needs reliability gates around Python, FastAPI, Playwright, or MCP workflows, send the bottleneck to [melbinjpaulose@gmail.com](mailto:melbinjpaulose@gmail.com?subject=Agent%20workflow%20or%20tooling).
If you run a 24/7 local agent yourself, I would love to hear what wakes yours up.
