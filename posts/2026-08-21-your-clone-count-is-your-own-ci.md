---
title: Your GitHub clone count is mostly your own CI
description: 301 clones from 17 unique cloners looked like adoption. One extra API call showed every clone day was a day the repository ran its own workflows. Here is how to check yours.
date: 2026-08-21
slug: your-clone-count-is-your-own-ci
---
GitHub's traffic page said one of my repositories had **301 clones from 17 unique cloners** in a
fortnight. Seventeen different machines, and the tool had barely been announced. That is what
early adoption is supposed to look like.

It was the CI. All of it.

## The one call that killed it

The traffic endpoint gives you clones by day:

```bash
gh api repos/OWNER/REPO/traffic/clones --jq '.clones[] | "\(.timestamp[:10]) \(.count) \(.uniques)"'
```

The obvious next question, which I had not asked for two weeks, is whether those are the same
days your own workflows ran:

```bash
gh api "repos/OWNER/REPO/actions/runs?per_page=100" \
  --jq '.workflow_runs[].created_at[:10]' | sort -u
```

Line the two lists up. Mine did not roughly correlate. It matched exactly, in both directions:

| Day | Clones | Unique cloners | Our workflow runs |
|---|---|---|---|
| 04 to 09 Aug | 0 | 0 | 0 |
| 10 Aug | 16 | 2 | 1 |
| 11 Aug | 45 | 1 | 3 |
| 12 Aug | 0 | 0 | 0 |
| 13 Aug | 15 | 1 | 1 |
| 14 Aug | 75 | 1 | 5 |
| 15 Aug | 0 | 0 | 0 |
| 16 Aug | 0 | 0 | 0 |
| 17 Aug | 150 | 16 | 9 |

Every day with clones ran CI. Every day with CI had clones. Every other day recorded **zero
clones**, not few, zero. The clone count even tracks the run count: nine runs on the busiest
day, and the largest clone total of the fortnight sitting under it.

Nine of the fourteen days in a fortnight that looked like early adoption had no activity on the
repository at all.

(The daily unique counts add up to more than the 17 for the period. That is not an error in
either: GitHub deduplicates uniques across the window it is asked for, so a cloner seen on two
days counts twice by day and once for the fortnight. It is the same reason you cannot sum a
week of unique visitors and get the week's figure.)

## Why the unique count is the worse half

The total was never very convincing on its own. It was `17 unique cloners` that made it look
like people, and that number is the one to distrust most.

**A GitHub Actions checkout is a clone, and each runner is a different cloner.** Runners are
ephemeral machines, so a repository that runs a five-job matrix twice a day manufactures ten
"unique cloners" a day, forever, without a single human being involved. The number that looks
hardest to fake is the one your own CI inflates fastest.

A second repository of mine reported 68 unique cloners over the same fortnight, and it is the
more interesting case, because there the answer was **mostly** rather than **entirely**. Its
three biggest clone days are its three heaviest CI days, in that order. But seven other days
recorded a handful of clones each with no workflow run at all.

That distinction is the whole point of doing the split. One repository came back as pure
machinery. The other came back as machinery plus a thin real tail, and the tail is the part
worth knowing about.

## The number to compute instead

Neither raw figure is worth reading, so I stopped reading them. The one my watcher prints now
is **human clone days**: days that recorded clones and no workflow run of ours.

    docproof   0 human clone days
    rigout     7 human clone days

The first number is honest and disappointing and took ten seconds to compute. The second says
something real: on seven days in that fortnight, somebody who was not a machine of mine pulled
that repository.

Be clear about the size of it. Those seven days carry **13 clones between them**, against 460
on the CI days, out of 473 for the fortnight. So the honest summary of the second repository is
not "it has traffic". It is "under three per cent of its clone volume is unexplained by our own
runners, spread thinly across half the days". That is a much smaller and much more useful thing
to know than 68.

One trap on the way there, and it is closer than it looks. The runs endpoint pages at 100. Over
the fortnight above, the second repository had 65 runs, comfortably inside one page. Move the
same fourteen-day window forward by a single day and it returns **99**. One run short.

    2026-08-04..2026-08-17   65 runs
    2026-08-05..2026-08-18   99 runs

Nothing about that repository changed. The question changed by one day, and the answer went from
safely inside a page to one run from silently losing data off the end of it.

If you take a truncated first page as the complete list of CI days, days that *were* CI look like
days that were not, and your own runners get promoted to strangers. That error runs in the
flattering direction, which is the direction you are least likely to check. Report an incomplete
page as **unknown**, never as zero:

```bash
gh api "repos/OWNER/REPO/actions/runs?per_page=100" --jq '.total_count'
```

If that comes back at or above 100 for your window, page it properly before you trust the answer.

## PyPI does the same thing

The same evening I checked the package downloads, expecting them to be the clean number.
`pypistats` reported **87 downloads yesterday, 95 in the week, 233 in the month** for a small
Python package. Read as adoption, that is a package with pull.

The daily series took one more call. Between 1 July and 20 August 2026, a span of 51 days, that
package was downloaded 502 times. Only **35 of those days recorded a download at all**, and this
is where they landed:

| Day | Downloads | |
|---|---|---|
| 2026-07-01 | 110 | release |
| 2026-07-09 | 94 | release |
| 2026-08-17 | 87 | release |
| 2026-08-01 | 81 | release |
| 2026-07-11 | 13 | the best day that was not a release |
| The other 30 recorded days | 117 between them | median 3 |
| 16 further days | nothing recorded | |

**Four release days took 372 of 502 downloads, or 74 per cent.** The four biggest days of the
period are the four days a version was published, in a straight run before any ordinary day
appears. A typical day that registers at all is 3, and roughly a third of the calendar registers
nothing.

Publishing a release makes mirrors, caches and dependency bots fetch you. That is not demand, it
is the packaging ecosystem noticing a new version, and it lands entirely on days you can predict
from your own git tags.

So the number I track there is **the best non release day**. It only ever goes up, and when it
goes up it means somebody who was not a release pulled more of that package than ever before.

## The rule this leaves

Three headline numbers in one night, and every one of them was my own machinery reflected back
at me. That is not a coincidence about my projects. It is the ordinary condition of a small
project:

**Every distribution metric available to you is dominated by your own activity, and each one
reads as adoption until you split it.**

The split is one extra API call in every case. Which is the annoying part, because the reason I
had not made that call for two weeks was not that it was hard. It was that the unsplit number
was the one I wanted to be true.

Three questions worth an hour on your own repositories:

- Do your clone days line up with your workflow days?
- Do your download spikes line up with your release tags?
- Does the tool that shows you these numbers do the split for you, or are you doing it by
  remembering to?

If it is the third, you will stop remembering. Mine does the split itself now and prints the
honest figure, because the flattering one had already got as far as a draft pitch before anybody
checked it.
