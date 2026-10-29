# `packages/` — the shared layer of the Supabase monorepo

Repo: `santhoshkammari/supabase` (fork of `supabase/supabase`), branch `master`.
Scope: the 16 workspaces under `packages/`.

## 0. How this was read (method + caveats)

- Package list and per-package file counts came from the GitHub tree API via
  `fetch.py --tree packages/` → 965 tracked files under `packages/`, grouped by the
  second path segment.
- Every `package.json` under `packages/*` was fetched and read in full.
- A tarball of the same tree (`supabase-master.tar.gz`, branch `master`) was unpacked to
  `/tmp/opencode/extract/supabase-master` so cross-package greps (import counts, call-site
  counts) could be run locally. Two spot-checks confirmed the tarball is byte-identical to
  what the API served: `packages/pg-meta/src/pg-format/index.ts` and `packages/ui/package.json`
  both `diff` clean against the API-fetched copies.
- GitHub **code search** is unusable for this fork: `search/code` returns `total_count: 0`
  for every query (forks are not indexed). All "where is X used" claims below come from
  local `grep -rn` over the unpacked tree instead.
- Line numbers in citations are `path:line` in the `master` tree.

---

## 1. Package table

File counts are measured from the tracked tree (`find <pkg> -type f`). `src` = `.ts`/`.tsx`;
`tests` = `*.test.ts(x)`; `other` = everything else (CSS, JSON, SVG, woff, md, etc.).

| package.json `name` | dir | purpose (1 line) | files | src | tests | other | consumed by |
|---|---|---|---|---|---|---|---|
| `ui` | `packages/ui` | Shared React primitives (Radix + shadcn/ui) styled with Tailwind; the one component library every app uses | 194 | 161 | 13 | 20 | 8 apps + `ui-patterns`, `dev-tools`, `marketing` (11 consumers) |
| `ui-patterns` | `packages/ui-patterns` | Composite/product-level components (Admonition, CommandMenu, CodeBlock, PageHeader…), consumed by deep subpath imports | 269 | 227 | 34 | 8 | 8 apps (design-system, docs, kb, learn, lite-studio, studio, ui-library, www) |
| `common` | `packages/common` | Cross-app runtime: GoTrue auth client, feature flags (ConfigCat + PostHog), telemetry constants + PostHog client, theme provider, shared hooks | 99 | 66 | 11 | 22 | 7 apps + `ui-patterns`, `dev-tools` (9 consumers) |
| `pg-meta` | `packages/pg-meta` (`@supabase/pg-meta`) | SQL builders for Postgres catalog introspection, returning branded `SafeSqlFragment` values | 147 | 137 | 34 | 10 | **studio only** (1 consumer) |
| `api-types` | `packages/api-types` | Generated TypeScript types for the platform Management API (v1, v2, platform OpenAPI specs) | 15 | 5 | 0 | 10 | 4 apps + `common`, `ai-commands`, `ui-patterns`, `e2e/studio` (8 consumers) |
| `icons` | `packages/icons` | Custom Supabase brand SVG icon components, generated from `src/raw-icons/*.svg` | 87 | 42 | 0 | 45 | 5 apps + `ui-patterns` (6 consumers) |
| `marketing` | `packages/marketing` | Schema-driven campaign landing pages ("Go pages"), marketing forms, CRM clients (HubSpot / Customer.io / Notion) | 51 | 48 | 0 | 3 | **www only** (1 consumer) |
| `ai-commands` | `packages/ai-commands` | LLM features (docs RAG "clippy", SQL helpers) usable from Edge runtime via the `ai-commands/edge` subpath | 20 | 16 | 1 | 3 | docs, studio, www (3 consumers) |
| `config` | `packages/config` | The single Tailwind v4 config + shared CSS (base, colors, themes, typography, plugins) every app imports | 18 | 0 | 0 | 18 | 14 workspaces (all 8 apps + 6 packages) |
| `build-icons` | `packages/build-icons` (`@supabase/build-icons`) | CLI that turns a folder of SVGs into React components + an index file | 12 | 0 | 0 | 12 | `icons` only (1 consumer) |
| `dev-tools` | `packages/dev-tools` | Local/staging-only dev toolbar (telemetry inspector, flag overrides) that tree-shakes itself out of prod builds | 13 | 10 | 1 | 2 | docs, studio, www (3 consumers) |
| `docs-search` | `packages/docs-search` | Markdown → search-index ingester (splits MDX into rows and writes them to a Supabase table) | 9 | 7 | 2 | 0 | docs, kb (2 consumers) |
| `shared-data` | `packages/shared-data` | Static data shared by apps: pricing, plans, regions, extensions, error codes, log constants | 15 | 12 | 0 | 3 | docs, studio, www (3 consumers) |
| `eslint-config-supabase` | `packages/eslint-config-supabase` | Flat ESLint config (Next core-web-vitals + Turbo + TanStack Query + two custom Supabase rules) | 7 | 2 | 1 | 4 | 6 apps (design-system, docs, learn, studio, ui-library, www) |
| `generator` | `packages/generator` (`@supabase/generator`) | Standalone script that dereferences `$ref`s in the docs OpenAPI enrichments into flat JSON | 4 | 2 | 0 | 2 | **nothing** — no workspace depends on it (0 consumers) |
| `tsconfig` | `packages/tsconfig` | Shared tsconfig presets (`base.json`, `nextjs.json`, `react-library.json`) | 5 | 0 | 0 | 5 | 18 workspaces (every app + 9 packages) |

Total tracked files under `packages/`: **965**.

### Purpose evidence (one citation each)

- `ui` — `packages/ui/package.json:2` `"name": "ui"`; `packages/ui/README.md:3` "Supabase's shared React component library. Built on Radix UI primitives and shadcn/ui, styled with Tailwind CSS, and used across all Supabase apps."
- `ui-patterns` — `packages/ui-patterns/package.json:2`; `AGENTS.md:18` "Composite components — subpath imports, e.g. `ui-patterns/AssistantChat`".
- `common` — `packages/common/package.json:2`; `AGENTS.md:19` "Shared utils, telemetry constants, feature flags".
- `pg-meta` — `packages/pg-meta/package.json:2`; `packages/pg-meta/README.md:3-7` "SQL builders for Postgres catalog introspection … Each builder in `src/sql/` returns a safe, parameterized SQL fragment (`SafeSqlFragment`)".
- `api-types` — `packages/api-types/package.json:4` "Types shared between Supabase apps and packages"; `AGENTS.md:20`.
- `icons` — `packages/icons/package.json:2`; `packages/icons/README.md:3` "custom Supabase icons".
- `marketing` — `packages/marketing/package.json:4` "Reusable marketing sections and schemas for campaign landing pages".
- `ai-commands` — `packages/ai-commands/README.md:5-7` "This package contains all features involving AI and LLMs (eg. via OpenAI API)."
- `config` — `packages/config/package.json:2`; `DEVELOPERS.md` "All shared config".
- `build-icons` — `packages/build-icons/package.json:2,8-10` (a `bin` CLI named `build-icons`).
- `dev-tools` — `packages/dev-tools/index.ts:8-15` (tree-shaking pattern, local/staging only).
- `docs-search` — `packages/docs-search/package.json:28-30` (`exports: {"./ingest": "./src/ingest.ts"}`); `packages/docs-search/src/ingest.ts:16-23` `ingestMarkdown({ supabase, contentRoot, table })`.
- `shared-data` — `packages/shared-data/package.json:4` "Data shared between Supabase apps"; `packages/shared-data/index.ts:22-43`.
- `eslint-config-supabase` — `packages/eslint-config-supabase/next.js:60+` (`defineConfig([...])`).
- `generator` — `packages/generator/package.json:10-21` (12 `tsdoc:dereference:*` scripts pointing at `../../apps/docs/spec/enrichments/tsdoc_v{1,2}/*.json`).
- `tsconfig` — `packages/tsconfig/package.json:6` `"files": ["base.json", "nextjs.json", "react-library.json"]`.

---

## 2. Dependency graph

Built from every `package.json` in `packages/`, `apps/`, `blocks/`, `e2e/` (the `dependencies`,
`devDependencies`, `peerDependencies` blocks), filtered to `workspace:` versions.

### 2.1 Internal edges (package → package)

```
tsconfig ──────────────► (no workspace deps; leaf)
eslint-config-supabase ► (no workspace deps; leaf)
build-icons ───────────► (no workspace deps; leaf)
api-types ─────────────► (no workspace deps; leaf)
config ────────────────► (no workspace deps; leaf)
docs-search ───────────► (no workspace deps; leaf)
generator ─────────────► (no workspace deps; leaf)
shared-data ───────────► (no workspace deps; leaf)
pg-meta ───────────────► (no workspace deps; leaf)

icons ────────────────► build-icons
ui ───────────────────► (config*, tsconfig*)                 *devDeps only
common ───────────────► api-types, config                    (+tsconfig* devDep)
ui-patterns ──────────► common, icons, ui, tsconfig
dev-tools ────────────► common, ui
marketing ────────────► ui
ai-commands ──────────► config                                (+api-types*, tsconfig*)
```

### 2.2 Leaf packages (no workspace dependency at all)

`api-types`, `build-icons`, `config`, `docs-search`, `eslint-config-supabase`, `generator`,
`pg-meta`, `shared-data`, `tsconfig` — 9 of 16.

Evidence: `packages/*/package.json` contain no `workspace:` value other than `tsconfig`
in `devDependencies` (`packages/ui/package.json:50-51`, `packages/shared-data/package.json:12-13`,
`packages/docs-search/package.json:20-21`).

### 2.3 Used by more than one app (cross-app fan-out)

Measured by counting distinct consuming workspaces per package:

| package | # consuming workspaces | which |
|---|---|---|
| `tsconfig` | 18 | all 8 apps + 9 packages + `blocks/vue` + `e2e/studio` |
| `config` | 14 | all 8 apps + 6 packages |
| `ui` | 11 | all 8 apps + `ui-patterns`, `dev-tools`, `marketing` |
| `common` | 9 | 7 apps + `ui-patterns`, `dev-tools` |
| `api-types` | 8 | 4 apps + `common`, `ai-commands`, `ui-patterns`, `e2e/studio` |
| `ui-patterns` | 8 | 8 apps |
| `eslint-config-supabase` | 6 | design-system, docs, learn, studio, ui-library, www |
| `icons` | 6 | 5 apps + `ui-patterns` |
| `ai-commands` | 3 | docs, studio, www |
| `dev-tools` | 3 | docs, studio, www |
| `shared-data` | 3 | docs, studio, www |
| `docs-search` | 2 | docs, kb |
| `build-icons` | 1 | `icons` |
| `pg-meta` | 1 | studio |
| `marketing` | 1 | www |
| `generator` | 0 | — |

**The three "everyone" packages are `tsconfig`, `config`, `ui`.** Everything else is a
narrow, app-shaped slice.

### 2.4 Import-volume evidence (not just package.json)

- `import … from 'ui'` — **2383** occurrences across 12 workspaces
  (studio 1480, www 361, design-system 292, ui-patterns 95, docs 72, ui-library 30,
  learn 19, kb 18, marketing 12, dev-tools 2, lite-studio 1).
- `import … from 'ui-patterns/…'` — **2016** occurrences; the top subpaths are
  `ui-patterns/Admonition` (291), `ui-patterns/ShimmeringLoader` (282),
  `ui-patterns/form/FormItemLayout/FormItemLayout` (248), `ui-patterns/PageSection` (142),
  `ui-patterns/DataInputs/Input` (105).
- `import … from '@supabase/pg-meta'` — **349** occurrences, **307 of them in `apps/studio`**.
- `import … from 'api-types'` — **218** occurrences (studio 208, common 3, docs 3,
  ui-library 2, ui-patterns 1, www 1).

---

## 3. `packages/ui` — how components are published and consumed

### 3.1 Publication model: copy source, not copy-paste into apps

`packages/ui` is a **shadcn-style registry that lives in the monorepo**, not an npm package.

- `packages/ui/components.json:1-14` is a real shadcn config:
  `"$schema": "https://ui.shadcn.com/schema.json"`, `"aliases": { "components": "src/components/shadcn", "utils": "src/lib/utils" }`.
  So `npx shadcn add …` into `packages/ui` drops a source file under `packages/ui/src/components/shadcn/ui/`.
- There are **53 shadcn component source files + 7 test files** in
  `packages/ui/src/components/shadcn/ui/` (60 files total), plus **22** in-house component
  directories at `packages/ui/src/components/` (Button, SidePanel, Menu, TreeView, …).
- `packages/ui/index.tsx` is a **174-line barrel** with **103 `export` statements**, e.g.
  `index.tsx:46-59` re-exports `shadcn/ui/{dropdown-menu,sonner,separator,sheet,badge,input-otp,alert-dialog,avatar,drawer,menubar,navigation-menu,progress,skeleton,slider}`.
- Apps **import the source**, they do not vendor it: `import { Badge, Button, Input } from 'ui'`
  (`packages/ui/README.md:7-11`).
- `packages/ui/package.json:4-5` `"main": "./index.tsx"`, `"types": "./index.tsx"` — the package
  entry is **TypeScript source**, not compiled output.

### 3.2 Export map

`packages/ui` has **no `exports` field** in its `package.json`. Consequences:

- Only the barrel `ui` is the intended entry point.
- Deep imports still resolve, and 4 files in the repo use them:
  `ui/src/lib/utils/cn` (2), `ui/src/components/shadcn/ui/tooltip` (1),
  `ui/src/components/shadcn/ui/alert` (1). Because there is no `exports` map, nothing stops
  new deep imports.

`packages/ui-patterns` is the opposite — it has a **generated export map**:

- `packages/ui-patterns/package.json:15+` declares `exports` with **194 entries**, each
  `{ "import": "./src/…", "types": "./src/…" }`, plus 3 entries with a `"style"` condition
  for `.css` files.
- The map is machine-written: `packages/ui-patterns/scripts/update-exports.ts:15-46` walks
  `src/`, and `:48-61` rewrites `package.json` (`"gen:exports": "tsx ./scripts/update-exports.ts"`,
  `packages/ui-patterns/package.json:13`). `update-exports.ts:36-41` adds the `style`
  condition only for `.css` "because tailwind resolves css @import with the 'style' condition only".

### 3.3 Theming / Tailwind setup

The theme lives in **CSS custom properties**, not in a JS theme object.

- Source of truth: `packages/ui/build/css/source/semantic.css`. It defines *inputs*
  (`--hue`, `--chroma`, `--surface`, `--foreground-lightness`, `--contrast`,
  `--muted-foreground-level`, `--tertiary-foreground-level`) at
  `semantic.css:11-45`, and derives every semantic colour from them in **OKLCH**.
- Per-theme overrides: `packages/ui/build/css/themes/dark.css` and `light.css`
  (dark at `dark.css:1-13` sets `--hue: 157.5`, `--chroma: 0.005`, `--surface: 0.19`;
  light at `light.css:1-20` sets `--surface-hue-offset: 180` for the complementary canvas tint).
- Both theme files key off `[data-theme='dark']` / `.dark` and `[data-theme='light']` / `.light`.
- The runtime switch is `next-themes`: `packages/common/Providers.tsx:19-33` renders
  `<NextThemesProvider themes={['dark','light']} value={THEME_DOM_VALUES} defaultTheme="system" enableSystem disableTransitionOnChange>`,
  with `THEME_DOM_VALUES = { dark:'dark', light:'light', 'classic-dark':'dark' }`
  (`packages/common/theme.ts:1-5`) and a legacy-theme migration shim (`Providers.tsx:8-17`).
- Tailwind wiring: `packages/config/tailwind.config.css:13-17` imports
  `../ui/build/css/source/global.css`, `semantic.css`, `compat.css`, then `themes/dark.css`
  and `themes/light.css`; `:27-34` adds the colour/theme/chart/animation/utilities layers.
  `packages/config/tailwind.config.css:3-7` registers `@tailwindcss/typography`,
  `@tailwindcss/forms`, `tw-animate-css` as Tailwind v4 `@plugin`s.
- `packages/ui/tailwind.config.css:1-4` is **only a stub for the VS Code Tailwind extension**:
  "@import 'config/tailwind.config.css'". The README says the same
  (`packages/ui/README.md:44`): "The workspace root owns the actual `tailwind.config.js`."

### 3.4 How apps consume it (the CSS half matters)

Every app has a `globals.css` that does three things:

1. `@import 'config/tailwind.config.css'` (+ `inline-code.css`, `typography.css`) —
   e.g. `apps/studio/styles/globals.css:1-3`.
2. Declares `@source` globs for its own code **and** for the shared packages, because
   Tailwind v4 scans only the files it is told about:
   `apps/studio/styles/globals.css:7-8`
   `@source './../../../packages/ui/src/**/*.{tsx,ts,js}'` and
   `@source './../../../packages/ui-patterns/src/**/*.{tsx,ts,js}'`.
   The same two lines exist in design-system (`globals.css:10-11`), docs (`:16-17`),
   learn (`:5-6`), lite-studio (`:6-7`), ui-library (`:8-9`), www (`:11-12`).
   `apps/kb/src/styles/globals.css` does **not** list them (Astro/Vite Tailwind plugin, different setup).
3. Overrides Tailwind tokens per app, e.g. `apps/studio/styles/globals.css:14-25` rescales
   `--radius*` "by 4/3 to match the Studio curve".

The TS half: every app lists `"ui": "workspace:*"` and `"ui-patterns": "workspace:*"` in
`dependencies` (`apps/studio/package.json`, `apps/www/package.json`, …).

### 3.5 `ui` conventions enforced in-repo

`AGENTS.md:51`: "import from `'ui'`; primitives are shadcn/ui-based and exported unsuffixed
(`Input`, `Select`, `Form`, …). Use `Button` — the in-house component … Check
`packages/ui/index.tsx` before creating new primitives. Higher-level patterns live in
`packages/ui-patterns`."

`packages/ui/README.md:13` claims "Some of the components have the `_Shadcn_` suffix" —
this is **stale**: `grep -rn "_Shadcn_" packages/ui/src` returns **0** hits, and the shadcn
button is exported as plain `Button` (`packages/ui/src/components/shadcn/ui/button.tsx:60`
`export { Button, buttonVariants }`). 26 call sites in the repo do use `Button_Shadcn`
(see below, gotcha 5).

---

## 4. `packages/pg-meta` — what `SafeSqlFragment` solves

### 4.1 The problem

`packages/pg-meta` builds SQL that runs against **the user's own live Postgres catalog**
(Studio's Table Editor, Database pages, entity lists, definitions). Because it runs against
arbitrary user schemas, a naive template-literal builder is an injection vector.

The package's own README frames the whole design: "Each builder in `src/sql/` returns a safe,
parameterized SQL fragment (`SafeSqlFragment`) that a caller executes against a user's live
database to read schema metadata" (`packages/pg-meta/README.md:3-7`).

### 4.2 The mechanism: a branded string type

`packages/pg-meta/src/pg-format/index.ts`:

- `:27` — `export type SafeSqlFragment = string & { readonly __safeSqlFragmentBrand: never }`
- `:36` — `export type UntrustedSqlFragment = string & { readonly __untrustedSqlFragmentBrand: never }`
- `:39` — `export type DisplayableSqlFragment = SafeSqlFragment | UntrustedSqlFragment`

A plain `string` is **not assignable** to `SafeSqlFragment`, so the type system blocks
accidental interpolation. The four sanctioned ways to produce one:

| producer | line | what it does |
|---|---|---|
| `safeSql` template tag | `:359-367` | `strings.reduce(...)` — the signature is `...interpolated: Array<SafeSqlFragment>`, so a plain string inside `` safeSql`…` `` is a **compile error** |
| `ident(value)` | `:93-134` | Postgres identifier quoting (ported from `libpq`); doubles `"` → `""`; leaves valid unquoted identifiers alone; rejects `null`/`undefined`/objects |
| `literal(value)` | `:138-213` | Postgres literal quoting; doubles `'` → `''`, doubles `\` and prefixes `E`; `NULL`, booleans, `Infinity`, `NaN`, and `::jsonb` casts handled |
| `keyword(value)` | `:227-237` | allow-list: single word matching `/^[A-Za-z][A-Za-z0-9_]*$/`, or one of `ALLOWED_MULTI_WORD_KEYWORDS = { 'INSTEAD OF', 'BY DEFAULT' }` (`:219`). Anything else **throws** |
| `joinSqlFragments(frags, sep)` | `:404-409` | joins already-branded fragments with a fixed `SqlFragmentSeparator` (`:41-55`) |

Two "escape hatches" exist, deliberately narrow:

- `rawSql(sql)` (`:374-376`) — "Marks a user-provided SQL string as a SafeSqlFragment …
  Only use this when the user has explicitly typed or authored the SQL".
- `untrustedSql(sql)` (`:383-385`) — brands third-party-influenced SQL as **untrusted**,
  safe to display, not safe to execute.
- `acceptUntrustedSql(sql)` (`:396-398`) — "Promote SQL to executable after explicit user
  acknowledgment … ONLY call from an event handler tied to a deliberate user action
  (onClick, keydown on Run shortcut). Never call from useEffect, render, or any path that
  runs without a user gesture."

### 4.3 Where the type is enforced at runtime

`apps/studio/data/sql/execute-sql-mutation.ts` is the execution boundary:

- `:48-64` — `type ExecuteSqlVariables = { … sql: SafeSqlFragment … }`
- `:76` — `export async function executeSql<T = any>({ … })`

So a raw string or an `UntrustedSqlFragment` **fails to compile** at `executeSql`.
The repo documents this in `.agents/skills/safe-sql-execution/SKILL.md:220-224`:
"SQL run against the user's Postgres database runs through the `executeSql` function, which
only takes arguments of type `SafeSqlFragment` for the SQL parameter. Raw strings or
`UntrustedSqlFragment`s will error at compile time."

The same skill (`:36-106`) defines the three provenance classes — hardcoded (`safeSql`),
third-party-influenced (`untrustedSql`), user-authored (`rawSql`) — and `:149-181` documents
that `acceptUntrustedSql` "MUST ONLY BE USED IN event handlers".

### 4.4 Builder usage in the package

- `packages/pg-meta/src/helpers.ts:24-34` — `filterByList()` builds
  `safeSql`IN (${joinSqlFragments(include.map(literal), ',')})`` — the include list goes
  through `literal`, never raw.
- `packages/pg-meta/src/helpers.ts:16` — `coalesceRowsToArray` interpolates a table name via
  `ident(source)`.
- `packages/pg-meta/src/sql/tables.ts:19-23` — `getTablesSql(targetOid?: SafeSqlFragment)`
  composes three optional scopes through `safeSql`.
- `packages/pg-meta/src/query/QueryAction.ts:9,51` — `select(columns?: SafeSqlFragment)`:
  even the fluent `query.from('t').select('*')` builder types the column list as a branded
  fragment.
- `packages/pg-meta/src/index.ts:36-46` re-exports the whole toolbelt plus the three brands.

### 4.5 The second, non-security concern: plan guards

`packages/pg-meta/README.md:12-46` documents a *performance* rule: introspection queries run
against a catalog of unknown size ("A real production catalog had ~267K `pg_class` rows"), and
unscoped CTEs turned one Table Editor open into "30–58s of work, tripping statement timeouts".
The package therefore ships a **plan guard** test suite
(`packages/pg-meta/test/db/stress-catalog.ts`, `test/db/plan-guard.ts`,
`test/sql/studio/catalog-plan-guard.test.ts`), and README.md:35-46 makes it a hard rule:

> Every new introspection query added under `src/sql/` that runs on a user's live catalog
> **must** get a budget entry in `test/sql/studio/catalog-plan-guard.test.ts`.

### 4.6 Where it is used

- `apps/studio` only: 349 import sites, 307 of them in `apps/studio`
  (all `apps/studio/data/**`).
- The brand appears in 333 places across **99 files** in `apps/studio`.
- `apps/studio/data/table-rows/operation-queue-save-mutation.ts:1,41,97-104` — builds queued
  DML with `safeSql` + `joinSqlFragments`.
- `apps/studio/data/content/notebooks/notebook-schema.ts:1,205` — notebook cells typed
  `SafeSqlFragment`; `unchecked_sql` typed `UntrustedSqlFragment`.
- `apps/studio/lib/ai/tools/approval-gate.ts:1,14` — the AI tool approval gate wraps
  `acceptUntrustedSql` so the model cannot auto-run SQL.

### 4.7 The parallel analytics brand (worth knowing)

Analytics SQL (BigQuery / ClickHouse) deliberately uses a **different** brand,
`SafeLogSqlFragment`, in `apps/studio/data/logs/safe-analytics-sql.ts`. Reason given in
`.agents/skills/safe-sql-execution/SKILL.md:402-407`: "The brands are kept separate because
escape semantics differ — Postgres-safe `E'…'` strings, `::jsonb` casts, and double-quoted
identifiers are unsafe for BigQuery and/or ClickHouse, and vice versa."

---

## 5. `packages/common` — auth, telemetry, flags, runtime config

`packages/common/index.tsx` (17 lines) is the barrel: `auth`, `configcat`, `consent-state`,
`constants`, `database-types`, `enabled-features`, `feature-flags`, `gotrue`, `helpers`,
`hooks`, `markdown-affordance`, `MetaFavicons/pages-router`, `Providers`,
`first-referrer-cookie`, `safe-storage`, `telemetry`, `telemetry-utils`.

### 5.1 Auth client (GoTrue)

`packages/common/gotrue.ts`:

- `:183-194` — the shared client:
  ```ts
  export const gotrueClient = new AuthClient({
    url: process.env.NEXT_PUBLIC_GOTRUE_URL,
    storageKey: STORAGE_KEY,
    detectSessionInUrl: shouldDetectSessionInUrl,
    debug: debug ? (persistedDebug ? logIndexedDB : true) : false,
    lock: navigatorLockEnabled ? debuggableNavigatorLock : undefined,
    experimental: { recoveryCodes: true },
    ...('localStorage' in globalThis ? { storage: globalThis.localStorage, userStorage: globalThis.localStorage } : null),
  })
  ```
- `:5` — `STORAGE_KEY = process.env.NEXT_PUBLIC_STORAGE_KEY || 'supabase.dashboard.auth.token'`.
- `:26-41` — debug/persisted-debug/navigator-lock flags are all gated on
  `process.env.NEXT_PUBLIC_IS_PLATFORM === 'true'`, and read localStorage through a
  `try/catch` helper (`:18-24`) because Safari throws on `localStorage` access.
- `:129-181` — `debuggableNavigatorLock` wraps `navigatorLock` with a 10-second watchdog that
  broadcasts on a `BroadcastChannel` to find the tab holding the lock.

`packages/common/auth.tsx` is the React layer:

- `:58-63` `AuthContext`, `:69-123` `AuthProvider` (calls `gotrueClient.initialize()` and
  subscribes to `onAuthStateChange`), `:127-156` `useAuth`/`useSession`/`useUser`/`useIsLoggedIn`/
  `useIsMFAEnabled`, `:158-163` `signOut`/`logOut` (`logOut` also calls `clearLocalStorage()`),
  `:172-185` `getAccessToken()` (server-side returns `undefined`).

Note `auth.tsx:131-140`: `useUser()` returns `null` when auth-js hands back its
`__isUserNotAvailableProxy` (user storage not yet migrated), instead of crashing on property access.

### 5.2 Feature flags

Two providers, merged in one React context — `packages/common/feature-flags.tsx`:

- `:26-49` `getFeatureFlags(API_URL, {organizationSlug, projectRef})` → `GET {API_URL}/platform/telemetry/feature-flags`
  (PostHog). Response typed from the API spec: `:23-24`
  `components['schemas']['TelemetryCallFeatureFlagsResponse_Output']`.
- `:51-56` `trackFeatureFlag(...)` → `POST /platform/telemetry/feature-flags/track`, gated on
  `hasConsented()`.
- `:99-114` `FeatureFlagProvider` props: `enabled?: boolean | { cc: boolean; ph: boolean }`.
- `:176-191` — both providers load **in parallel** with `Promise.allSettled` so one failure
  does not block the other.
- `:133-160` `ensureGroupContext()` → `POST /platform/telemetry/identify` with
  `{ user_id, organization_slug, project_ref }` and a `Version: '2'` header; deduped by a ref.
- `:199-203` — dev-toolbar cookie overrides (`x-ph-flag-overrides`, `x-cc-flag-overrides`,
  `vercel-flag-overrides`) are applied only when `process.env.NEXT_PUBLIC_ENVIRONMENT` is
  `local` or `staging`.
- `:293` — ConfigCat values are additionally pushed into `flags/react`'s `<FlagValues>` so
  the `flags` library and `useFlag` agree.
- `:307-322` — `useFlag(name)` returns `false` when the store is empty **or** the key is
  missing (and logs `Flag key "…" does not exist in ConfigCat flag store`).

ConfigCat client — `packages/common/configcat.ts`: `:16-57` `getClient()` prefers
`NEXT_PUBLIC_CONFIGCAT_PROXY_URL` (with `waitForReady()` and a `NoFlagData` check, falling
back to the SDK key), poll interval 7 minutes (`:27`); `:78-99` `getFlags()` injects an
`is_staff` custom attribute derived from `@supabase.` in the email (`:82`).

### 5.3 Telemetry

- `packages/common/telemetry-constants.ts` — **4420 lines**, **232 `export interface`** event
  shapes and a union type `TelemetryEvent` at `:4188`. Header comment (`:1-12`) states the
  naming rules: past-tense verbs only, new verbs need `@growth-eng` review, and the
  canonical list lives in the platform repo.
- `packages/common/telemetry.tsx` (509 lines) — the client side: `TelemetryTagManager`
  (`:48-73`) injects Google Tag Manager only when `IS_PLATFORM && NEXT_PUBLIC_GOOGLE_TAG_MANAGER_ID && hasAccepted`;
  `:75-120` `getFirstTouchAttributionProps` maps UTM params and click-ids
  (`gclid`, `gbraid`, `wbraid`, `msclkid`, `fbclid`, `rdt_cid`, `ttclid`, `twclid`, `li_fat_id`,
  `bfcid`, `oppref`) into PostHog properties.
- `packages/common/posthog-client.ts` (458 lines) — the PostHog client and
  `buildSessionRecordingConfig`.
- `packages/common/consent-state.ts`, `consented-url-cookie.ts`, `first-referrer-cookie.ts`,
  `telemetry-first-touch-store.ts`, `telemetry-utils.ts` — consent gating and first-touch attribution.

Studio consumes them: `apps/studio/lib/telemetry/track.ts:1-2`
(`import { sendTelemetryEvent } from 'common'`, `import { TelemetryEvent, TelemetryGroups } from 'common/telemetry-constants'`).

### 5.4 Shared runtime config

- `packages/common/constants/environment.ts:1-2`
  ```ts
  export const IS_PLATFORM = process.env.NEXT_PUBLIC_IS_PLATFORM === 'true'
  export const IS_PROD = process.env.NEXT_PUBLIC_VERCEL_ENV === 'production'
  ```
- `packages/common/constants/local-storage.ts:3-153` — a **153-key** `LOCAL_STORAGE_KEYS`
  catalogue (Studio / Common / Docs / WWW sections) plus a 27-key allowlist (`:157-184`) that
  `clearLocalStorage()` (`:186-192`) preserves on sign-out.
- `packages/common/safe-storage.ts:1-84` — `safeLocalStorage` / `safeSessionStorage` wrappers
  that swallow Safari/quota errors and dedupe console warnings.
- `packages/common/enabled-features/` — a **different** flag mechanism from ConfigCat/PostHog:
  `enabled-features.json` is a static build-time list; `index.ts:24` defines
  `Feature = RuntimeFeature | keyof typeof enabledFeaturesStaticObj`; `:50-83` `isFeatureEnabled()`
  merges static-disabled features with runtime `disabled_features` from the user profile;
  `overrides.ts:28-58` lets server-only `ENABLED_FEATURES_*` env vars force-disable a feature
  (used to build a filtered docs search index, `index.ts:59-66`).
- `packages/common/theme.ts:1-9` — `THEME_DOM_VALUES` + `migrateLegacyTheme`.
- `packages/common/Providers.tsx:19-33` — the `next-themes` wrapper.
- `packages/common/hooks/` — 19 shared hooks; `useParams.ts:12` imports
  `next/compat/router` (see gotcha 2).

---

## 6. `packages/api-types` — generation, sync, consumption

### 6.1 The three specs

`packages/api-types/redocly.yaml:1-13` maps three OpenAPI documents to three `.d.ts` outputs:

| spec | local URL (for `codegen`) | production URL (for `codegen:prod` / `verify`) | committed output |
|---|---|---|---|
| `api-v1` | `http://localhost:8080/api/v1-json` | `https://api.supabase.com/api/v1-json` | `types/api-v1.d.ts` (14 568 lines) |
| `api-v2` | `http://localhost:8080/api/v2-json` | `https://api.supabase.com/api/v2-json` | `types/api-v2.d.ts` (11 956 lines) |
| `platform` | `http://localhost:8080/api/platform-json` | `https://api.supabase.com/api/platform-json` | `types/platform.d.ts` (36 121 lines) |

Total generated TypeScript: **62 645 lines** across the three `.d.ts`, plus
`types/fga-requirements.ts` (305 lines).

### 6.2 How types are generated

`packages/api-types/package.json:10`:
```
"codegen": "openapi-typescript --redocly ./redocly.yaml --alphabetize --default-non-nullable=false && node ./scripts/generate-fga-requirements.mjs && prettier --cache --write types/*.d.ts types/fga-requirements.ts"
```
- `openapi-typescript` produces the `.d.ts`; `--alphabetize` keeps the diff stable.
- `--default-non-nullable=false` makes optional fields `| null` rather than optional.
- Prettier is applied **last** so the committed files match the repo's format config.

`packages/api-types/package.json:11-12` add two production-driven scripts:
```
"codegen:prod": "node ./scripts/generate-production-types.mjs"
"verify-production-types": "node ./scripts/verify-production-types.mjs"
```

`packages/api-types/scripts/generate-production-types.mjs:13-24` fetches the three production
specs into a temp dir, generates into `types/` **directly** ("no diffing — it always writes",
per the skill doc).

`packages/api-types/scripts/verify-production-types.mjs`:
- `:13-23` — spec list + `platformApiUrl` override via `PLATFORM_API_OPENAPI_URL`, 30 s fetch timeout.
- `:25-52` `fetchOpenApiSpecifications` — writes each spec to a temp file and builds a temp `redocly.yaml`.
- `:54-71` `findMismatchedTypes` — byte-compares generated vs committed for
  `api-v1.d.ts`, `api-v2.d.ts`, `platform.d.ts`, `fga-requirements.ts`.
- `:73-121` `reportTypeDifferences` — `diff -u` with `committed/` and `production/` labels, and
  writes an escaped HTML summary to `$GITHUB_STEP_SUMMARY`.
- `:128-193` `generateTypes` — runs `pnpm exec openapi-typescript` then `pnpm exec prettier`.
  `:171-178` explains a subtle trap: "Prettier resolves its config from the formatted file's
  location. The generated files live in a temporary directory outside the repository, so pass
  the repository config explicitly or they are formatted with Prettier's defaults and never
  match the committed files."
- `:195-215` `verifyProductionTypes` — generates into a throwaway dir, diffs, and on mismatch
  throws `"Committed API types do not match production: …"` (`:210`).

### 6.3 FGA (fine-grained authorization) requirements

`packages/api-types/scripts/fga-requirements.mjs` reads the `x-fga-permissions` OpenAPI
extension off every operation (`:40-74`), validates each permission against the
`CreateScopedAccessTokenBody.properties.permissions.items.enum` list (`:3-13`, `:15-38`),
rejects duplicate endpoints across specs (`:57-61`), and emits a sorted constant map
(`:82-99`). The output header (`packages/api-types/types/fga-requirements.ts:1-4`) says:
"Generated by `pnpm --filter=api-types codegen:prod` … Do not edit by hand. … A caller needs
every permission in at least one group (OR between groups, AND within a group). Keys are the
path literals passed to openapi-fetch."

### 6.4 How they stay in sync with production

Three layers:

1. **Local dev codegen** — `pnpm api:codegen` (root `package.json:53`) reads
   `http://localhost:8080` (needs a running local API).
2. **Production codegen** — `pnpm api:codegen:prod` (root `package.json:54`) reads
   `https://api.supabase.com/api/*-json` and overwrites the committed files.
3. **CI gate** — `.github/workflows/verify-production-api-types.yml`:
   - `:19` — the job only runs when the PR touches `packages/api-types/(types|scripts)/`.
   - `:46` — `pnpm install --frozen-lockfile --filter=api-types...`.
   - `:50` — `pnpm --filter=api-types run verify-production-types`.
   So the check fires only on PRs that *edit* the generated files — a plain app PR that
   silently drifts from production is **not** caught by this job.

The repo also ships a machine-readable procedure: `.agents/skills/api-types/SKILL.md:10-19`
("1. Make the API/schema change and ensure it is deployed to production … 3. Inspect and commit
only the intended generated type changes. 4. Run `pnpm api:verify-types`"),
`:21-25` ("A pass means the committed generated declarations match all three production specs
at the time of the check"), and `:27-29` ("The `Verify production API types` CI job … is a
required merge check").

`AGENTS.md:47` forbids hand-editing: "Never hand-edit generated files: `packages/api-types/types/**` …".

### 6.5 How apps consume them

`packages/api-types/index.ts` merges the three specs into one type surface:

- `:19-20` — `export interface paths extends apiV2Paths, apiV1Paths, platformPaths {}`
- `:21-36` — `export interface components { schemas: apiV2 & apiV1 & platform, responses: …, parameters: …, requestBodies: …, headers: …, pathItems: … }`
- `:38` — also re-exports `platformComponents`, `apiV1Components`, `apiV2Components` separately.
- `:40-41` — re-exports the generated `fgaRequirements` map and its types.

The consumer pattern is **openapi-fetch** (218 import sites of `api-types`):

`apps/docs/lib/fetch/fetchWrappers.ts`:
```ts
1: import type { paths } from 'api-types'
2: import createClient from 'openapi-fetch'
13: const client = createClient<paths>({ baseUrl: API_URL, … })
34: client.use({ async onRequest({ request }) { … } })   // adds X-Request-Id + Bearer token
45: export const { GET: get, POST: post } = client
```

`apps/studio/data/fetchers.ts:4,31-44` does the same (`createClient<paths>`), with an
important wrinkle at `:6`: `import type { paths } from './api'` — a **local** shim
`apps/studio/data/api.d.ts` whose whole body is:
```ts
/**
 * Avoid importing this file and import the types directly from api-types
 * @deprecated import from 'api-types' instead
 */
export type * from 'api-types'
```
`openapi-fetch` is declared in three apps' `package.json`: studio (`"openapi-fetch": "0.12.4"`),
docs, ui-library.

Two documented runtime sharp edges in `apps/studio/data/fetchers.ts`:
- `:67-76` — "openapi-fetch only treats a response body as empty when `status === 204` or the
  response carries a `Content-Length: 0` header; otherwise it calls `response.json()`, which
  throws 'Unexpected end of JSON input' … HTTP/3 (and HEAD requests) may omit `Content-Length: 0`
  on empty-body responses — e.g. a `201` with no body — so a request that succeeds over HTTP/2
  can fail over HTTP/3." The fix is `normalizeEmptyBodyResponse` (`:77-100`).
- `:2` — `import { DEFAULT_PLATFORM_APPLICATION_NAME } from '@supabase/pg-meta/src/constants'`
  — a **deep import into a package that has no `exports` map**.

---

## 7. Build and publish model

### 7.1 Nothing is published to npm

Measured over all 16 `packages/*/package.json`:

- `publishConfig`: **absent in all 16**.
- `"private": true` in only 4: `build-icons`, `dev-tools`, `tsconfig`, and the root.
- No `.npmrc` at the repo root.
- No `npm publish` / `pnpm publish` / `registry.npmjs` reference anywhere in `.github/` or `scripts/`.
- **No package has a `build` script.** (Checked every `scripts` block: `hasBuild=False` for all 16.)

Versions are placeholders: `ui` `0.0.0`, `common` `0.0.0`, `pg-meta` `0.0.0`; `icons` and
`ui-patterns` have **no `version` field at all**; `build-icons` is `1.0.0`;
`eslint-config-supabase` is `1.0.0`.

**Conclusion: every package is consumed as TypeScript/CSS source through the pnpm workspace.**

### 7.2 Workspace mechanics

- `pnpm-workspace.yaml:1-5` — `packages: [apps/*, packages/*, blocks/*, e2e/*]`.
- `pnpm-workspace.yaml:13-60` — a **`catalog:`** section pins shared third-party versions once
  (`react: ^19.2.6`, `next: ^16.3.6`, `tailwindcss: ^4.2.4`, `lucide-react: ^1.55.0`,
  `@supabase/supabase-js: 2.117.3`, …). Packages reference them as `"react": "catalog:"`
  (`packages/ui/package.json:27`, `packages/ui-patterns/package.json`), which is how a
  12-package tree stays on one React version.
- `pnpm-workspace.yaml:28-33` — a documented catalog trap: `typescript` stays aliased to the
  `~6.0.2` compat package while `@typescript/native` provides the native TS 7 `tsc` binary,
  because "TypeScript 7 has no programmatic API until 7.1".
- `pnpm-workspace.yaml:10-11` — `enableGlobalVirtualStore: false` with the reason
  "Doesn't work because of Typescript issues with peer dependencies, see pnpm#9739".
- Local cross-links use `workspace:*` (e.g. `packages/common/package.json:16` `"api-types": "workspace:*"`).

### 7.3 Turbo

`turbo.jsonc:5-29` defines only six tasks: `build` (`dependsOn: ["^build"]`),
`lint`, `clean` (`cache: false`), `dev` (`persistent: true`), `test` (`cache: false`),
`typecheck` (`dependsOn: ["^typecheck"]`). `cacheMaxAge: "14d"`.

Because **no package defines a `build` task**, the `^build` dependency edge is a no-op for
the packages — the shared layer contributes nothing to the build cache; it is compiled by
each app's own bundler (Next.js / Vite / Astro) as source.

Root scripts (`package.json:10-56`) that matter for packages:
- `test:ui` → `turbo run test --filter=ui` (`:32`), `test:ui-patterns` (`:33`).
- `typecheck` → `turbo --continue typecheck` (`:26`) — `typecheck` is defined per package
  (e.g. `packages/ui/package.json:9`, `packages/pg-meta/package.json:13-14`).
- `api:codegen` / `api:codegen:prod` / `api:verify-types` (`:53-55`).

### 7.4 Per-package test/lint tooling

- `packages/ui` — vitest (`packages/ui/package.json:11-13`), 13 test files under `src/`.
- `packages/ui-patterns` — vitest, 34 test files.
- `packages/pg-meta` — `"test": "test/run-tests.sh vitest run --coverage"`
  (`packages/pg-meta/package.json:11`) — a shell wrapper that spins up a **real Postgres**
  (`packages/pg-meta/test/db/docker-compose.yml`, `Dockerfile`, `00-init.sql`, `01-memes.sql`).
  `test/db/stress-catalog.ts` builds a synthetic 2000-table catalog for the plan guard
  (`packages/pg-meta/README.md:29-33`).
- `packages/api-types` — `"test": "node --test ./scripts/*.test.mjs"` (`:13`), 4 test files.
- `packages/common` — vitest, 11 test files (e.g. `configcat.test.ts`, `safe-storage.test.ts`).

---

## 8. Failure modes and gotchas

### Gotcha 1 — `pnpm --filter ui generate-tailwind-classes` is broken

`packages/ui/package.json:11` offers `"generate-tailwind-classes": "tsx ./scripts/generate-tailwind-classes.ts"`,
but `packages/ui/scripts/generate-tailwind-classes.ts:3` does
`const color = require('./../../build/css/tw-extend/color')`, and
`packages/ui/build/css/` contains only `source/` and `themes/` — **no `tw-extend/`**.

Reproduced locally:
```
$ node -e "require('./scripts/generate-tailwind-classes.ts')"
Error: Cannot find module './../../build/css/tw-extend/color'
```

**Symptom:** the script exits non-zero with `Cannot find module './../../build/css/tw-extend/color'`.
Anyone trying to regenerate `src/lib/tailwind-demo-classes.ts` (which is committed and still
imported by `packages/ui/index.tsx:173`) is blocked. The file it writes already exists, so
nothing in CI breaks — the script is simply dead. The Tailwind v4 CSS-first system replaced
the old JS colour map.

### Gotcha 2 — `packages/common`'s barrel pulls in Next.js; two apps can't use it

`packages/common/index.tsx:16` re-exports `./telemetry`; `packages/common/telemetry.tsx:4-6`
imports `next/compat/router`, `next/navigation`, `next/script`. `packages/common/index.tsx:10`
re-exports `./hooks`; `packages/common/hooks/index.ts:16` re-exports `./useParams`, and
`packages/common/hooks/useParams.ts:12` imports `next/compat/router`.
`packages/common/package.json:47` declares `"next": "catalog:"` as a **peerDependency**.

But `apps/kb` (Astro) and `apps/lite-studio` (React Router + Vite) depend on `common`
without depending on `next` — verified: `apps/kb/package.json` has no `next` in
`dependencies` or `devDependencies`.

Consequence: the two non-Next apps may only use **deep** imports. The only `common` import
in kb is `apps/kb/src/layouts/Layout.astro:3` → `import { genFaviconLinks } from 'common/MetaFavicons/icons'`.
There are **zero** `from 'common'` barrel imports in `apps/kb` or `apps/lite-studio`.

**Symptom:** someone writes `import { useCopy } from 'common'` in the Astro app and the build
fails with `Can't resolve 'next/compat/router'` / `Module not found: Can't resolve 'next/script'`
— a confusing error for an app that has no Next.js at all.

### Gotcha 3 — `packages/ui` and `packages/ui-patterns` have broken `main` fields

- `packages/ui-patterns/package.json:3-4` — `"main": "./index.tsx"`, `"types": "./index.tsx"`,
  but **there is no `index.tsx`** at `packages/ui-patterns/` (the directory contains only
  `README.md`, `package.json`, `scripts/`, `src/`, `tailwind.config.css`, `tsconfig.json`,
  `vitest.*`).
- `packages/generator/package.json:4-5` — `"main": "./index.tsx"` — also **missing**
  (`packages/generator/` contains `helpers.ts`, `package.json`, `tsconfig.json`, `tsdoc.ts`).
- `packages/config/package.json:4` — `"main": "index.js"` — **missing** (the package ships only
  CSS + a `postcss.config.js` + `typography.config.js`).
- `packages/tsconfig/package.json:4` — `"main": "index.js"` — **missing**.
- `packages/docs-search/package.json` — **no `main` at all**, and its `exports` map contains
  only `"./ingest"` (`:28-30`).

**Symptom:** `import x from 'ui-patterns'` (bare) resolves to a non-existent `index.tsx` and
the bundler errors "Module not found" / "export 'x' was not found". Today this is latent:
the repo has exactly **1** bare `ui-patterns` import and it is inside a comment
(`apps/studio/components/ui/InformationBox.tsx:19`), **0** bare `docs-search` imports, and
**0** `from 'config'` imports — apps consume `config` only as CSS (`@import 'config/tailwind.config.css'`).
But `packages/config` and `packages/tsconfig` advertise a `main` that does not exist, so
any new `import { something } from 'config'` is a build error waiting to happen.

### Gotcha 4 — Tailwind v4 needs an explicit `@source` per app, or shared components render unstyled

Tailwind v4 does not scan node_modules. Each app must declare the shared packages as
sources, or every class used **inside** `packages/ui` / `packages/ui-patterns` is purged.

All eight Next/Vite apps do this
(`apps/studio/styles/globals.css:7-8`, `apps/www/styles/globals.css:11-12`,
`apps/docs/styles/globals.css:16-17`, `apps/design-system/styles/globals.css:10-11`,
`apps/learn/styles/globals.css:5-6`, `apps/lite-studio/styles/globals.css:6-7`,
`apps/ui-library/styles/globals.css:8-9`). `apps/kb/src/styles/globals.css` does **not** —
Astro uses `@tailwindcss/vite` instead (`apps/kb/package.json` devDependencies).

**Symptom:** in a new app (or a new package) the shared `<Button>` renders with no padding,
no background and no border — the classes exist in the source but were never generated.
There is no error; it is purely visual.

### Gotcha 5 — the `ui` barrel has no `exports` map, and the README is stale

`packages/ui/package.json` has no `exports` field, so `ui/src/...` deep imports resolve
(4 already exist). More confusingly, `packages/ui/README.md:13` says
"Some of the components have the `_Shadcn_` suffix. These components should be preferred" —
but `grep -rn "_Shadcn_" packages/ui/src` returns **0** hits. The shadcn button is exported
as plain `Button` (`packages/ui/src/components/shadcn/ui/button.tsx:60`), while the in-house
one is also `Button` (`packages/ui/src/components/Button/Button.tsx`). 26 call sites in
apps use `Button_Shadcn` — so the *name* `Button_Shadcn` exists in app code but not in the
package README's description of it.

**Symptom:** a developer follows the README, hunts for `Button_Shadcn` in `packages/ui`, does
not find it, and either imports the wrong `Button` (breaking the design system) or adds a
new duplicate component.

### Gotcha 6 — `api-types` drift only fails CI on PRs that touch the package

`.github/workflows/verify-production-api-types.yml:19` gates the job on the PR touching
`packages/api-types/(types|scripts)/`. An app-only PR that depends on a changed production
API is **not** checked.

**Symptom:** `pnpm api:verify-types` locally prints
`Committed API types do not match production: platform.d.ts` and the diff shows a new
endpoint the app does not know about. The fix (per `.agents/skills/api-types/SKILL.md:21-25`)
is to deploy the API first, then run `pnpm api:codegen:prod` and commit the regenerated
files. A second, quieter failure mode: `verify-production-types.mjs:171-178` warns that
Prettier must be pointed at the repo config explicitly, otherwise the generated files are
formatted with Prettier defaults and the byte comparison fails even though the types are
semantically identical.

### Gotcha 7 — `keyword()` throws on anything that is not a single word

`packages/pg-meta/src/pg-format/index.ts:227-237` accepts only
`/^[A-Za-z][A-Za-z0-9_]*$/` or the two phrases in `ALLOWED_MULTI_WORD_KEYWORDS` (`:219`).

**Symptom:** `keyword('DROP TABLE')` throws
`Not a valid keyword: "DROP TABLE". Must be a single word matching [A-Za-z][A-Za-z0-9_]*, or one of: INSTEAD OF, BY DEFAULT.`
The same guard exists to stop "control phrases" from slipping through — but it will also
reject a legitimate two-word keyword you want to add, and the fix is to compose two
`keyword()` calls through `safeSql` instead.

### Gotcha 8 — `safeSql` type safety is compile-time only, and one cast defeats it

`safeSql` is a template tag: the *type* signature blocks plain strings, but the runtime
implementation (`packages/pg-meta/src/pg-format/index.ts:363-366`) is just string
concatenation. `rawSql` (`:374-376`) is a bare `as SafeSqlFragment` cast — a deliberate
escape hatch for user-authored SQL, and the skill file says it is
"pretty much the ONLY VALID USE CASE" (`.agents/skills/safe-sql-execution/SKILL.md:105-106`).
The same file warns about `as SafeSqlFragment` casts on stored snippet content
(`SKILL.md:360-370`).

**Symptom:** a developer writes `` safeSql`SELECT * FROM ${userInput}` `` and gets a red
squiggle (good), but then "fixes" it with `userInput as SafeSqlFragment` and ships an
injection. The type system cannot catch the cast.

### Gotcha 9 — `useFlag()` fails **closed** and logs an error for an unknown key

`packages/common/feature-flags.tsx:307-322`: if the ConfigCat store is empty (not loaded yet)
it returns `false`; if the key is missing it logs
`Flag key "<name>" does not exist in ConfigCat flag store` and returns `false`.

**Symptom:** a feature silently stays off with no UI signal, and the console shows one error
per render of the consuming component. If the flags never load (missing
`NEXT_PUBLIC_CONFIGCAT_SDK_KEY` / `NEXT_PUBLIC_CONFIGCAT_PROXY_URL`,
`packages/common/configcat.ts:19-25`), **every** flag is `false` forever.

### Gotcha 10 — `packages/common/gotrue.ts` silently creates an unusable client without `NEXT_PUBLIC_GOTRUE_URL`

`packages/common/gotrue.ts:184` — `url: process.env.NEXT_PUBLIC_GOTRUE_URL` with no default
and no guard. The module-level `new AuthClient(...)` at `:183` runs on import.

**Symptom:** in an app that forgets the env var, the auth client points at `undefined`, and
`gotrueClient.initialize()` / `getSession()` fails at request time with a confusing
network/URL error rather than a config error at boot. The same class of problem applies to
`NEXT_PUBLIC_IS_PLATFORM` (`packages/common/constants/environment.ts:1`) — it defaults to
`false`, which silently disables the whole platform code path.

### Gotcha 11 — `packages/generator` is orphaned

`packages/generator/package.json:10-21` defines 12 scripts whose paths point at
`../../apps/docs/spec/enrichments/tsdoc_v{1,2}/*.json`, but **no workspace lists
`@supabase/generator` as a dependency** (0 consumers). `grep -rn "@supabase/generator"`
across the whole repo returns only its own `package.json:2`.

**Symptom:** running `pnpm --filter @supabase/generator run tsdoc:dereference:gotrue:v1`
must be done from the repo root with the filter (the relative `../../apps/docs` path only
resolves from `packages/generator/`), and nothing in CI invokes it — the
`*_dereferenced.json` files can drift from the `*.json` sources unnoticed.

---

## 9. When to use this / when not to

### Use `packages/ui` when
- You need a primitive that already exists in `packages/ui/index.tsx` (103 export statements).
  Check the barrel first — `AGENTS.md:51`.
- You want the in-house `Button` (not the shadcn one) — it carries Supabase-specific
  `control-surface-shadows` and `focus-ring` classes (`packages/ui/src/components/Button/Button.tsx:26-28`).
- You are adding a *shadcn* primitive: run `npx shadcn add` into `packages/ui` (the
  `components.json` aliases point at `src/components/shadcn` and `src/lib/utils`), then
  re-export it from `packages/ui/index.tsx`.
- You are changing a theme: edit `packages/ui/build/css/themes/{dark,light}.css` (the *inputs*)
  or `packages/ui/build/css/source/semantic.css` (the derivation), never per-app overrides —
  but do check `packages/config/css/colors.css` and `theme.css`, which map the theme tokens
  to Tailwind utilities.

### Do not use `packages/ui` when
- You need a *composite* pattern (Admonition, CommandMenu, CodeBlock, PageHeader, form rows):
  use `packages/ui-patterns/<Name>` — the split is explicit in `AGENTS.md:51`.
- You are writing a one-off component for a single app. `packages/ui` is shared by 8 apps;
  every addition is a public surface for all of them.
- You want to escape the design system. `packages/ui/README.md:26` — "Tailwind only — no inline
  styles or CSS modules"; `README.md:27-31` — prefer semantic pairs
  (`bg-card text-card-foreground`) over hardcoded colours.

### Use `packages/pg-meta` when
- You are writing a Postgres catalog introspection query → add it under `packages/pg-meta/src/sql/`,
  return a `SafeSqlFragment`, **and** add a budget entry to
  `packages/pg-meta/test/sql/studio/catalog-plan-guard.test.ts` (mandatory per
  `packages/pg-meta/README.md:35-46`).
- You need to compose SQL for a user's DB → use `safeSql` + `ident`/`literal`/`keyword`.
- You are promoting SQL that came from the user or from an AI → `rawSql` / `untrustedSql` +
  `acceptUntrustedSql` inside an event handler only.

### Do not use `packages/pg-meta` when
- You are querying *your own* platform tables → use `openapi-fetch` with `api-types` paths.
- You are building analytics SQL for BigQuery/ClickHouse → that is the **separate**
  `SafeLogSqlFragment` brand in `apps/studio/data/logs/safe-analytics-sql.ts`, deliberately
  disjoint from the Postgres brand (`.agents/skills/safe-sql-execution/SKILL.md:402-407`).
- You want to pass a table/column name straight from a URL param → that is `untrustedSql`,
  not `safeSql`.

### Use `packages/common` when
- You need auth (`useAuth`, `useUser`, `getAccessToken`, `signOut`), feature flags
  (`useFlag`, `FeatureFlagProvider`), telemetry (`TelemetryEvent` union, `sendTelemetryEvent`),
  the theme provider, or the shared hook set.
- You are in a Next.js app. In a non-Next app (kb, lite-studio) use **deep** imports only
  (gotcha 2).

### Do not use `packages/common` when
- You need a *static* table (pricing, plans, regions, extensions, error codes) → `packages/shared-data`.
- You need a composite UI component → `packages/ui-patterns`.
- You need an icon → `packages/icons` (brand icons) or `lucide-react` (generic).

### Use `packages/api-types` when
- You call the platform Management API. Use `createClient<paths>` from `openapi-fetch` — that
  gives you typed paths, typed bodies, and typed responses for free.
- You need a response schema type → `components['schemas'][...]`, as
  `packages/common/feature-flags.tsx:22-24` does.

### Do not use `packages/api-types` when
- You want to change the types. They are generated; `AGENTS.md:47` forbids hand-editing.
  Deploy the API, then `pnpm api:codegen:prod`, then `pnpm api:verify-types`.
- You are writing a *new* endpoint definition. The spec lives in the platform repo, not here.

### Use `packages/ui-patterns` when
- You need a composite pattern, and you import it by subpath: `ui-patterns/Admonition`,
  `ui-patterns/CodeBlock`, `ui-patterns/form/FormItemLayout/FormItemLayout`.
- You are adding a new pattern: put the file under `packages/ui-patterns/src/<Name>/`, then run
  `pnpm --filter ui-patterns gen:exports` to regenerate the 194-entry export map.

### Do not use `packages/ui-patterns` when
- You want a primitive (→ `packages/ui`).
- You want the bare package (`import … from 'ui-patterns'`) — there is no `index.tsx`; the
  `main` field points at a file that does not exist (gotcha 3).

---

## 10. Open questions (unverified)

1. **Is `packages/ui`'s `_Shadcn_` suffix convention gone or just renamed?** The README says it
   exists; the source has zero matches; 26 app call sites use `Button_Shadcn`. I did not trace
   where `Button_Shadcn` is actually defined — it may live in `apps/studio` or in
   `packages/ui/src/components/shadcn/ui/button.tsx` under a different symbol. **Not measured.**
2. **How are `packages/ui-patterns` exports kept in sync in CI?** `scripts/update-exports.ts`
   rewrites `package.json`, but I found no workflow that runs `gen:exports` and fails on a
   stale map. A new file under `src/` may be silently unreachable until someone runs it.
   **Not measured.**
3. **Do the `packages/ui` Tailwind classes in `packages/ui/src` get generated in `apps/kb`?**
   kb's `globals.css` has no `@source` for the shared packages. Either Astro's
   `@tailwindcss/vite` plugin auto-scans them, or kb silently renders unstyled shared
   components. **Not measured** — I did not run kb's build.
4. **What is the actual consumer set of `packages/shared-data`'s `scoped-access-token-permissions.ts`?**
   The file header claims two consumers (Studio's PAT form and the docs generator
   `apps/docs/spec/sections/generateAccessControlPartials.mts`). I did not verify the docs side.
5. **Is `packages/docs-search` also used for the v2 search index?** `apps/docs/scripts/search_v2/ingest.ts:4`
   and `apps/kb/scripts/search/ingest.ts:5` both import `docs-search/ingest`, but the package
   itself has no notion of "v1" vs "v2". **Not measured.**
6. **Does `@supabase/pg-meta` get published to npm for `supabase/postgres-meta`?** Its
   `package.json` says `"repository": "supabase/supabase"` and the README says the builders are
   "shared by Supabase Studio and `postgres-meta`" — but there is no publish script in this
   repo. The publishing pipeline (if any) is external. **Not measured.**
7. **Exact per-app Tailwind class-generation counts** — I measured source files and import
   sites, not the generated CSS size. **Not measured.**
8. **`packages/ui` build/css ownership.** `packages/config/tailwind.config.css:13-17` imports
   from `../ui/build/css/…`, i.e. the `config` package depends on the `ui` package's files by
   **relative path**, not by a declared dependency. `packages/config/package.json` has no
   `ui` dependency. This works because both are in the same workspace, but it is an
   undeclared coupling. I did not find a build that would break it. **Not measured whether
   this is intentional.**

---

## Appendix A — measurement commands used

```bash
# package list + per-package file counts
python3 kb-work/fetch.py --tree packages/ | awk -F/ '{print $2}' | sort | uniq -c | sort -rn
cd packages && for d in */; do p=${d%/}; \
  total=$(find "$p" -type f | wc -l); \
  src=$(find "$p" -type f \( -name "*.ts" -o -name "*.tsx" \) | wc -l); \
  test=$(find "$p" -type f \( -name "*.test.ts" -o -name "*.test.tsx" \) | wc -l); \
  md=$(find "$p" -type f -name "*.md" | wc -l); echo "$p $total $src $test $md $((total-src-md))"; done

# dependency graph (from package.json only)
python3 -c "…for each package.json, collect workspace:* deps, invert…"

# import-site counts
grep -rn "from 'ui'"        apps/ packages/ --include=*.ts --include=*.tsx | wc -l   # 2383
grep -rn "from 'ui-patterns" apps/ packages/ --include=*.ts --include=*.tsx | wc -l   # 2016
grep -rn "from '@supabase/pg-meta'" apps/ packages/ --include=*.ts --include=*.tsx | wc -l  # 349
grep -rn "from 'api-types'" apps/ packages/ --include=*.ts --include=*.tsx | wc -l   # 218
```

## Appendix B — the shared layer at a glance

```
                    ┌─────────── apps (8) + blocks + e2e ───────────┐
                    │  studio   www   docs   kb   learn   design-system
                    │  ui-library   lite-studio
                    └───────────────────┬──────────────────────────┘
                                        │
   ┌──────────────┬─────────────┬───────┴───────┬──────────────┬─────────────┐
   │   config     │  tsconfig   │     ui       │ ui-patterns  │   common    │
   │ (tailwind+css)│ (ts presets)│ (primitives) │ (composites) │ (runtime)   │
   └──────────────┴─────────────┴───────┬───────┴──────┬───────┴──────┬──────┘
                                       │              │              │
                                 ┌─────┴─────┐   ┌────┴────┐   ┌────┴─────┐
                                 │ dev-tools │   │ icons   │   │ api-types│
                                 │ marketing │   │    └────┴────┐│           │
                                 └───────────┘   │ build-icons│└───────────┘
                                                 └────────────┘
   studio-only:  @supabase/pg-meta        standalone: @supabase/generator (0 consumers)
   docs+kb:      docs-search
```
