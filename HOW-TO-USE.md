# HOW-TO-USE

How to get value back out of this repo.

## Find an item

```bash
# by keyword
grep -rin "aria2" items/

# by area
grep -l "area: infra" items/*.md

# list everything, newest first
ls -t items/
```

`index.md` is the table of contents. It has one row per item with area, status
and source. Read that first, then open the item.

## Use it in research or writing

Pull items into a prompt instead of re-reading sources:

```
Read /disk2/santhosh/knowledge-base/index.md, then open the items tagged <area>.
Give me: the key mechanism, the measured numbers, the failure modes, and the
limits. Cite item paths for each claim.
```

For a written answer, ask for the claims with their labels (`[checked]`,
`[source]`, `[memory]`) so you can see the weak spots.

## Add material from X while scrolling

Fast path, two commands:

```bash
# 1. save the post (text or link) with the date
echo "https://x.com/xxx/status/123
why: the retry/backoff trick is worth keeping" >> inbox/$(date +%F)-$(echo x-post | tr ' ' '-').md

# 2. later, process it into an item
#    follow HOW-TO-WRITE.md
```

Sweep the feed whenever a post looks reusable. One line in `inbox/` is enough
at capture time. Processing happens later, in batches.

## Add a paper

```bash
echo "arxiv:2404.xxxxx  <title>" >> inbox/$(date +%F)-<slug>.md
```

Then read: abstract, method, results, limitations. Cite section numbers.

## Cadence

| when | what |
|---|---|
| daily | sweep X and papers, drop raw captures into `inbox/` |
| weekly | process `inbox/` into items, update `index.md`, push |
| monthly | revisit items marked `draft`, mark `evergreen` when they age well |

## Status labels

- `draft` — written, depth bar not met yet.
- `reviewed` — depth bar met, verified.
- `evergreen` — re-checked after months and still accurate.

## Rules for using an item as a source

- An item is a summary, not the source. For anything load-bearing, follow its
  source links back to the original.
- `[memory]` claims in an item are unverified. Re-check them before you rely on them.
- Numbers age. Check the "last verified" date in the item front matter.

## Feedback loop

When an item proves wrong or outdated, fix it in place and add a `### Changes`
entry with the date and what changed. History stays visible.
