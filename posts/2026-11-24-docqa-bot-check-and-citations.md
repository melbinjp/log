---
title: How DocQA blocks bot walls, bounds vision scans, and cites pages
description: Three DocQA_api fixes reject challenge pages, judge scans across the document in a 75s budget, and cite pages in each sentence.
date: 2026-11-24
slug: docqa-bot-check-and-citations
---
A document Q&A session fails quietly when the fetch layer stores the wrong file.
It also fails when the reader stalls past the HTTP request window.
Three fixes in [DocQA_api](https://github.com/melbinjp/DocQA_api) close those paths at ingest and answer generation.

When a user sent a tenancy agreement URL, the host served the PDF to browsers.
The same host sent an HTML verification gate and a placeholder PDF to the server.
Every stage ran without error.
The session kept the requested URL label while its index held unrelated text.

The [bot-wall guard](https://github.com/melbinjp/DocQA_api/commit/b2dbe9e) adds `looks_like_a_bot_wall` in `utils/url_fetch.py`.
It checks extracted payloads up to 2,500 characters (`_BOT_WALL_MAX_CHARS`) against seven challenge markers.
Example markers include "Please wait while your request is being verified" and "Enable JavaScript and cookies to continue".
When a marker matches, ingest returns HTTP 400.
The response tells the user to download and upload the file.
Real long documents stay safe because the check stops above 2,500 characters.

A second failure hit a 75-page paper (GPT-3) with HTTP 504 timeouts on URL ingest.
A per-page check treated three low-text figure pages as scanned pages.
Those three pages triggered a three-model fallback ladder with a 90s per-attempt timeout and no total deadline.

The [vision-budget fix](https://github.com/melbinjp/DocQA_api/commit/6ac24b6) moves `pages_for_vision` in `utils/vision.py` to a document threshold (`SCANNED_PAGE_FRACTION = 0.5`).
Under scanned mode, a document triggers page transcription only when half or more pages have no text.
Figure pages in text-heavy papers therefore stay with their captions.
In `transcribe_pages`, each attempt drops to 40s.
An `asyncio.wait_for` cap (`VISION_BUDGET_SECONDS = 75.0`) ends the pass cleanly inside one request.

Page numbers previously appeared only in the eight source cards below the answer.
Readers had to match each claim to an excerpt by hand.
The [citation prompt update](https://github.com/melbinjp/DocQA_api/commit/4a1a5a1) in `app.py` (`generate_rag_response`) fixes this gap.
It directs the model to cite `(page 4)` or `(report.pdf, page 4)` inside the claim sentence.
The prompt restricts labels to the excerpt headings.
For unpaged files such as HTML or plain text, it names the document only.

The live tool runs at [docqa.wecanuseai.com](https://docqa.wecanuseai.com).
Regression tests live in `tests/test_url_ingest.py` and `tests/test_vision.py`.

If your team needs help with document pipelines, agent tools, or backend reliability, send the workflow, failure, and required result to [melbinjpaulose@gmail.com](mailto:melbinjpaulose@gmail.com?subject=Document%20pipeline%20or%20agent%20tooling).
For a role, include the scope, location, and assessment format.
I am based in Kozhikode, India.
