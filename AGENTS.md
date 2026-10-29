# AGENTS.md

Rules for this knowledge base. Applies to me, and to any agent that writes here.

## What this repo is

A personal knowledge base. Items are distilled learning notes. The value is in
depth and traceability, not in volume. One item per topic, written once, well.

## Non-negotiable rules

1. **One item per file.** `items/YYYY-MM-DD-slug.md`. Never one big file with many topics.
2. **Cite everything load-bearing.** Each claim that carries weight points at:
   - a file and line in a repo (`apps/studio/pages/...tsx:42`),
   - a URL plus the date you read it,
   - or a paper with section/figure/table.
3. **Label the evidence.** Use `[checked]` (you ran or read it), `[source]` (a doc or page says so, with its date), `[memory]` (training data, unverified). Never present `[memory]` as fact.
4. **Honest depth.** Say what you did NOT check. Mark open questions in the item.
5. **No secrets.** No tokens, keys, private URLs, personal data of other people.
6. **No AI attribution.** Commit messages read like a human wrote them. Never add a `Co-Authored-By` trailer.
7. **Index stays true.** If you add or change an item, update `index.md` in the same commit.
8. **No invented detail.** If you could not verify a number, say "not measured" or "my estimate". Never smooth over a gap.
9. **Never rewrite history.** Items get corrected in place with a `### Changes` note, not by deleting history.

## Item anatomy

Every item file starts with front matter:

```yaml
---
title: <short human title>
date: YYYY-MM-DD
type: repo | paper | post | talk | book | concept | tool
area: <one tag, e.g. infra, llm, frontend, databases>
status: draft | reviewed | evergreen
source: <primary URL or repo path>
tags: [tag, tag]
---
```

Then these sections, in this order:

1. **One-paragraph summary.** What it is and why I care. Three to six sentences.
2. **What it is** — the concrete shape: files, stack, versions, entry points.
3. **How it works** — the mechanism, step by step, with `file:line` refs.
4. **Key numbers** — a table of measured facts (size, speed, counts). Source each row.
5. **Failure modes / gotchas** — what breaks, and the symptom it produces.
6. **When to use it / when not to.** Honest boundaries.
7. **Open questions.** What I did not verify.
8. **Related items.** Links to other items in `index.md`.
9. **Sources.** Every URL with the date read.

## Depth bar (what "deep" means)

An item passes only if it has all of these:

- At least 5 concrete references (`file:line`, URL, table, figure).
- At least 3 numbers that were measured or read from a primary source.
- At least 2 failure modes with the symptom you would actually observe.
- A clear "do not use this when" line.
- At least 1 open question, unless the topic was fully verified.

If you cannot meet the bar, write it as `status: draft` in `inbox/` and say why.

## Workflow

1. **Read** the source properly. Code first, then docs, then blog posts about it.
2. **Capture** raw material into `inbox/YYYY-MM-DD-slug.md` if you are not ready to write the item.
3. **Verify** the load-bearing claims. Run the command, read the file, fetch the page.
4. **Write** the item in `items/`.
5. **Index** it: add a row to `index.md`.
6. **Commit** with the format below, then push.
7. **Tell me.** One short mail, same subject thread.

## Commit format

```
kb: add <topic> item (<type>)

<one paragraph: what it covers and the key takeaway>
```

## Quality checklist before push

- [ ] Front matter complete, `date` real
- [ ] Every claim labelled `[checked]` / `[source]` / `[memory]`
- [ ] Depth bar met (5 refs, 3 numbers, 2 failure modes, boundaries, open questions)
- [ ] No secrets, no AI attribution
- [ ] `index.md` updated
- [ ] Links inside the item resolve (relative paths for items, links for sources)

## Agent prompt (ready to paste)

```
Read /disk2/santhosh/knowledge-base/AGENTS.md and follow it exactly.
Target: <repo path / URL / paper>.
Deliverable: one item file in items/, plus the index.md row, plus a commit and push.
Rules: cite file:line for code claims, label [checked]/[source]/[memory], hit the depth bar,
never guess a number, and state what you did not verify.
```

## Repo map

- `items/` — finished learning items
- `modules/` — source snapshots copied as ordinary files; do not use Git submodules or copy nested `.git/`
- `research/` — detailed source-reading notes linked from learning items
- `inbox/` — raw captures, unprocessed
- `templates/` — item and row templates
- `meta/SOURCES.md` — where new material comes from
- `index.md` — table of contents
