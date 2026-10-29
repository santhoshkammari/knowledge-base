# Sources I watch

Where new material comes from. Each line is a capture target.

| source | type | how I get it | what I want from it |
|---|---|---|---|
| X (Twitter) | posts | agent-browser on the logged-in Chrome | paper announcements, build stories, tool releases, hard-won lessons |
| arXiv | papers | arxiv skill | new methods worth reusing |
| GitHub repos | repos | git clone + read | architecture worth copying, agent conventions worth stealing |
| Blog posts | posts | webfetch | mechanism-level explanations, not marketing |
| Talks / videos | talks | youtube skill | design decisions and failure stories |

## Capture rule

Capture into `inbox/` first. Process into `items/` later.

Capture a source when it contains at least one of:

- a mechanism I can re-implement,
- a number I can reuse,
- a failure mode I have hit,
- an agent workflow rule I can adopt.

Skip the rest. Volume is not the goal.

## Currently watched

| source | detail | status |
|---|---|---|
| supabase/supabase | monorepo fork at santhoshkammari/supabase | studied 2026-10-22, see items/2026-10-22-supabase-monorepo.md |
| Harvard CS224 | transcripts and ASR scripts at santhoshkammari/cs224-transcripts | copied as a source module in modules/cs224-transcripts/ (source commit a2836894dd492a7dc6485ba0675576238c6fa3e1) |
| X feed | personal timeline | swept on demand |

## Adding a source

Add one row. Say how you get it and what you want from it. Keep the "what I
want" column honest, otherwise the capture stops being worth it.
