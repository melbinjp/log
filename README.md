# log.wecanuseai.com

Working notes from building and running AI agents on real repositories, at
**[log.wecanuseai.com](https://log.wecanuseai.com)**.

Every claim in a post carries a receipt: a commit, a pull request, or a measurement you can
re-run. Where a post gives a number it also gives the command that produced it.

## How it is built

`posts/*.md` in, static HTML out. One script, one dependency:

```bash
pip install markdown
python build.py          # regenerate index.html, p/*.html, feed.xml, sitemap.xml
python build.py --check  # fail if the committed output does not match posts/
```

The generated files are committed, because GitHub Pages serves this directory with no build
step and a site that needs a toolchain to render is a site that breaks when the toolchain moves.
The cost of committing generated output is that it drifts from its source in silence, so
`--check` runs in CI on every push.

No client JavaScript, no web fonts, no analytics. The pages are text.

## Corrections

If something here is wrong, [open an issue](https://github.com/melbinjp/log/issues). A post that
turns out to be wrong gets corrected in place with the correction stated, not quietly deleted.
