# HOW-TO-WRITE

Step-by-step for adding a learning item. Works the same for me and for an agent.

## Step 0 — decide if it belongs here

An item belongs here when the source will still matter in 6 months and I will
not re-read the original. Skip: news, opinions with no mechanism, one-off fixes.

## Step 1 — capture fast (2 minutes)

Put the raw source into `inbox/` before you lose it.

```bash
cp notes.md inbox/2026-10-22-slug.md
```

Inbox files hold: the URL, the raw text or the key excerpt, why you saved it.
They are rough. Do not polish yet.

Naming: `inbox/YYYY-MM-DD-slug.md`.

## Step 2 — read the source properly

- Code: read the real files. Not the blog post about the code.
- Paper: read the method and results sections, plus the figures you cite.
- Post: find the thread behind it. Check if the claim holds up there.
- Repo: clone it, then read the entry points and the build config.

Keep notes as you go: `file:line`, numbers, and anything that surprised you.

## Step 3 — verify the load-bearing claims

For each claim you want to keep, get a primary source:

```bash
# code claim
grep -rn "max-num-seqs" apps/studio/vite.config.ts

# measured number
du -sh /disk1/models/Ornith-1.5-122B

# page claim (record the date)
curl -s https://example.com/page | head -40
```

Mark each claim `[checked]`, `[source]`, or `[memory]`.

## Step 4 — write the item

```bash
cp templates/item.md items/YYYY-MM-DD-slug.md
```

Fill every section. If a section has nothing, say why in it. Empty sections are
allowed only with an explicit "not applicable because ..." line.

## Step 5 — update the index

Add one row to `index.md` in the same commit as the item:

```markdown
| 2026-10-22 | [Supabase monorepo](items/2026-10-22-supabase.md) | repo | infra | reviewed | fork of supabase/supabase |
```

## Step 6 — commit and push

```bash
git add -A
git commit -m "kb: add supabase monorepo item (repo)

Deep read of the Supabase monorepo fork: pnpm+Turbo workspace, Studio stack,
self-hosted docker stack, and the agent conventions the repo itself ships."
git push origin master
```

Commit format: `kb: add <topic> item (<type>)`, then one paragraph.

## Step 7 — tell me

One mail, same subject thread, with: item name, path, one-line takeaway, link.

## Common mistakes

| mistake | fix |
|---|---|
| item too shallow, no file refs | read the code, quote `file:line` |
| claim without a source | add the source or label it `[memory]` |
| `index.md` forgotten | add the row before commit |
| numbers guessed | measure them, or write "not measured" |
| inbox file left forever | process it or delete it |
| personal data from other people | remove it |
