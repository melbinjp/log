#!/usr/bin/env python3
"""Build log.wecanuseai.com from posts/*.md.

    python build.py            # write index.html, p/<slug>.html, feed.xml
    python build.py --check    # build, then fail if anything on disk would change

Every generated file is committed. That is deliberate: GitHub Pages serves this directory
with no build step, so the site cannot break because a build tool changed under it. The cost
of committing generated output is that it drifts from its source without anyone noticing, so
`--check` runs in CI and fails when the committed HTML is not what the current posts produce.

Front matter is `key: value` lines between two `---` fences. Required: title, date,
description. Optional: `slug` (defaults to the filename after the date).
"""
from __future__ import annotations

import html
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
POSTS = ROOT / "posts"
OUT_POSTS = ROOT / "p"

SITE = "https://log.wecanuseai.com"
TITLE = "The Log"
TAGLINE = "Working notes from building and running AI agents on real repositories."
# The editorial rule, stated where a reader can hold me to it.
PROMISE = ("Every claim here carries a receipt: a commit, a pull request, or a measurement "
           "you can re-run.")

MONTHS = ("January February March April May June July August September October November "
          "December").split()


def read_post(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise SystemExit(f"{path.name}: no front matter")
    _, front, body = raw.split("---", 2)
    meta = {}
    for line in front.strip().splitlines():
        if ":" not in line:
            raise SystemExit(f"{path.name}: front matter line is not key: value -> {line!r}")
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    for required in ("title", "date", "description"):
        if not meta.get(required):
            raise SystemExit(f"{path.name}: front matter needs {required}")
    stem = path.stem
    meta["slug"] = meta.get("slug") or re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    meta["body"] = body.strip()
    meta["path"] = f"/p/{meta['slug']}.html"
    meta["url"] = SITE + meta["path"]
    meta["dt"] = datetime.strptime(meta["date"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    d = meta["dt"]
    meta["date_human"] = f"{d.day} {MONTHS[d.month - 1]} {d.year}"
    return meta


def render_markdown(body: str) -> str:
    return markdown.markdown(body, extensions=["fenced_code", "tables", "attr_list"])


def page(inner: str, *, title: str, description: str, canonical: str,
         is_post: bool) -> str:
    """One shell for every page. No client JavaScript anywhere on this site: the pages are
    text, and text does not need a runtime to arrive."""
    e = html.escape
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{e(canonical)}">
<meta name="author" content="Melbin J Paulose">
<meta property="og:type" content="{'article' if is_post else 'website'}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}">
<meta property="og:site_name" content="{e(TITLE)}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="application/rss+xml" title="{e(TITLE)}" href="{SITE}/feed.xml">
<link rel="icon" href="https://favicon.wecanuseai.com/favicon.ico">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header>
  <a class="wordmark" href="/">{e(TITLE)}</a>
  <nav>
    <a href="https://wecanuseai.com/">wecanuseai.com</a>
    <a href="/feed.xml">RSS</a>
    <a href="https://github.com/melbinjp/log">Source</a>
  </nav>
</header>
<main>
{inner}
</main>
<footer>
  <p>{e(PROMISE)}</p>
  <p class="what">What the writing is about, mostly:
     <a href="https://github.com/melbinjp/docproof">docproof</a>, which reports the claims a
     repository's documentation makes that its code contradicts;
     <a href="https://github.com/melbinjp/rigout">rigout</a>, an MCP server that lets an
     authorised agent use a real machine; and
     <a href="https://jules-prompts.wecanuseai.com/">jules-prompts</a>, a library of
     machine-readable task prompts for coding agents.</p>
  <p>Written while doing the work, by <a href="https://wecanuseai.com/">Melbin J Paulose</a>.
     Corrections are welcome as
     <a href="https://github.com/melbinjp/log/issues">issues</a>: if something here is wrong I
     would rather fix it than keep it.</p>
</footer>
</body>
</html>
"""


def build_index(posts: list[dict]) -> str:
    e = html.escape
    rows = []
    for p in posts:
        rows.append(
            f'<li class="entry">\n'
            f'  <a class="entry-title" href="{p["path"]}">{e(p["title"])}</a>\n'
            f'  <p class="entry-desc">{e(p["description"])}</p>\n'
            f'  <time datetime="{p["date"]}">{p["date_human"]}</time>\n'
            f'</li>'
        )
    inner = (
        f'<section class="intro">\n'
        f'  <h1>{e(TITLE)}</h1>\n'
        f'  <p class="tagline">{e(TAGLINE)}</p>\n'
        f'  <p class="promise">{e(PROMISE)}</p>\n'
        f'</section>\n'
        f'<ol class="entries">\n' + "\n".join(rows) + '\n</ol>'
    )
    return page(inner, title=f"{TITLE} - {TAGLINE}", description=TAGLINE,
                canonical=SITE + "/", is_post=False)


def build_post(p: dict) -> str:
    e = html.escape
    inner = (
        f'<article>\n'
        f'  <h1>{e(p["title"])}</h1>\n'
        f'  <p class="byline"><time datetime="{p["date"]}">{p["date_human"]}</time></p>\n'
        f'{render_markdown(p["body"])}\n'
        f'  <p class="back"><a href="/">All entries</a></p>\n'
        f'</article>'
    )
    return page(inner, title=f'{p["title"]} - {TITLE}', description=p["description"],
                canonical=p["url"], is_post=True)


def build_feed(posts: list[dict]) -> str:
    e = html.escape
    items = []
    for p in posts:
        stamp = p["dt"].strftime("%a, %d %b %Y 00:00:00 +0000")
        items.append(
            f"  <item>\n"
            f"    <title>{e(p['title'])}</title>\n"
            f"    <link>{e(p['url'])}</link>\n"
            f"    <guid isPermaLink=\"true\">{e(p['url'])}</guid>\n"
            f"    <pubDate>{stamp}</pubDate>\n"
            f"    <description>{e(p['description'])}</description>\n"
            f"  </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        '<channel>\n'
        f"  <title>{e(TITLE)}</title>\n"
        f"  <link>{SITE}/</link>\n"
        f"  <description>{e(TAGLINE)}</description>\n"
        '  <language>en</language>\n'
        f'  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n'
        + "\n".join(items) + "\n</channel>\n</rss>\n"
    )


def build_sitemap(posts: list[dict]) -> str:
    urls = [f"  <url><loc>{SITE}/</loc></url>"]
    for p in posts:
        urls.append(f"  <url><loc>{html.escape(p['url'])}</loc>"
                    f"<lastmod>{p['date']}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def main() -> int:
    check = "--check" in sys.argv
    sources = sorted(POSTS.glob("*.md"))
    if not sources:
        raise SystemExit("no posts found")
    posts = sorted((read_post(s) for s in sources),
                   key=lambda p: (p["date"], p["slug"]), reverse=True)

    written = {
        ROOT / "index.html": build_index(posts),
        ROOT / "feed.xml": build_feed(posts),
        ROOT / "sitemap.xml": build_sitemap(posts),
    }
    for p in posts:
        written[OUT_POSTS / f'{p["slug"]}.html'] = build_post(p)

    stale = []
    for path, text in written.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == text:
            continue
        stale.append(path.relative_to(ROOT).as_posix())
        if not check:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    # Say what was read, not just that it worked. A build that prints "done" and a build that
    # found no posts at all look identical from the outside.
    print(f"read {len(sources)} post(s) from posts/, wrote {len(written)} file(s)")
    if check and stale:
        print("STALE, the committed output does not match posts/:", file=sys.stderr)
        for s in stale:
            print(f"  {s}", file=sys.stderr)
        print("run: python build.py", file=sys.stderr)
        return 1
    if check:
        print("committed output matches posts/")
    elif stale:
        print("updated: " + ", ".join(stale))
    else:
        print("nothing changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
