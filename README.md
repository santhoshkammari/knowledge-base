# Knowledge Base

Personal, durable notes. One file per learning item. Every claim cites a source.

Built for one job: when I read something good (an X post, a paper, a repo, a talk),
I want it distilled once, in depth, so I can use it later without re-reading.

## How to use it

| want | do |
|---|---|
| see everything | [index.md](index.md) |
| add a new item | [HOW-TO-WRITE.md](HOW-TO-WRITE.md) |
| use it in research / writing | [HOW-TO-USE.md](HOW-TO-USE.md) |
| hand work to an agent | [AGENTS.md](AGENTS.md) |

## Layout

```
index.md            the table of contents, always current
AGENTS.md           rules for humans and agents: how to read, write, verify, commit
HOW-TO-WRITE.md     step-by-step: capture -> verify -> item -> index -> push
HOW-TO-USE.md       retrieval patterns, prompts, cadences
items/              one file per learning item
modules/            source snapshots copied as files; no Git submodules
research/           deep source-reading notes that support an item
inbox/              raw captures, not yet processed
templates/          file templates
meta/               sources I watch (X accounts, paper feeds, repos)
```

## Rules (short version)

1. One item per file. File name `items/YYYY-MM-DD-slug.md`.
2. Every load-bearing claim cites a source: `path:line`, a URL, or a paper section.
3. Claims are labelled `[checked]`, `[source]`, or `[memory]`.
4. Depth bar: real numbers, real file paths, real failure modes, and when **not** to use it.
5. No secrets, no private keys, no personal data from other people.
6. No AI attribution in commits.
7. `index.md` and the item's front matter change in the same commit as the item.

Full rules: [AGENTS.md](AGENTS.md).

## Items

- [Supabase monorepo](items/2026-10-22-supabase-monorepo.md) — 2026-10-22 — repo study
  - Supporting notes: [build system](research/supabase/build-system.md), [Studio](research/supabase/studio.md), [shared packages](research/supabase/packages.md).

## Modules

- [CS224 transcripts](modules/cs224-transcripts/README.md) — 33 tracked files copied from commit `a2836894dd492a7dc6485ba0675576238c6fa3e1`; the standalone source repo was deleted after verifying the snapshot.
