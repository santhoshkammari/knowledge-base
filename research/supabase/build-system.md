# 1 — Build system, workspace config and CI/tooling

**Repo:** `https://github.com/santhoshkammari/supabase` (fork of `supabase/supabase`), branch `master`
**Tree SHA read:** `8ba2f0a63bc6d9cc00886557ffa027c5e8a83cfc` (via GitHub trees API; tree not truncated)
**Method:** every file below was fetched from the GitHub contents API and cached under `/tmp/opencode/ghcache/`.
All line numbers are from those cached files. Numbers labelled "measured" were counted by script over the
full file tree / lockfile, not estimated.

---

## Key numbers

| Metric | Value | Source |
| --- | --- | --- |
| Workspace globs | **4** — `apps/*`, `packages/*`, `blocks/*`, `e2e/*` | `pnpm-workspace.yaml:1-5` |
| Workspace packages | **29** total importers in `pnpm-lock.yaml` = root `.` + **28** workspace projects | `pnpm-lock.yaml` `importers:` block |
| — apps | 8 (`design-system`, `docs`, `kb`, `learn`, `lite-studio`, `studio`, `ui-library`, `www`) | tree |
| — packages | 16 (`ai-commands`, `api-types`, `build-icons`, `common`, `config`, `dev-tools`, `docs-search`, `eslint-config-supabase`, `generator`, `icons`, `marketing`, `pg-meta`, `shared-data`, `tsconfig`, `ui`, `ui-patterns`) | tree |
| — blocks | 1 (`@supabase/vue-blocks`) | tree |
| — e2e | 4 (`e2e-docs`, `e2e-shared`, `e2e-studio`, `e2e-www`) | tree |
| Internal dependency edges (pkg → pkg) | **98** (94 × `workspace:*`, 2 × `workspace:^`, 2 × `workspace:`) | measured over the 29 `package.json` files |
| GitHub Actions workflows | **56** files in `.github/workflows/` | measured |
| — PR-triggered | **28** | measured |
| Turbo config files | **9** (root `turbo.jsonc` + one per app) | measured |
| Turbo version | **2.9.14** | `package.json:74` |
| pnpm | **11.13.1** (`packageManager`), engines `pnpm: 11.13` | `package.json:88`, `package.json:84` |
| Node | **22** (`.nvmrc`), engines `node: >= 22.13` | `.nvmrc:1`, `package.json:85` |
| TypeScript | `typescript: ~6.0.2` + `@typescript/native: npm:typescript@~7.0.2` (TS 7 native `tsc`) | `pnpm-workspace.yaml:33`, `pnpm-workspace.yaml:56` |
| pnpm catalog entries | **41** | `pnpm-workspace.yaml:13-61` |
| pnpm `overrides` entries | **24** | `pnpm-workspace.yaml:104-131` |
| pnpm `allowBuilds` entries | **24** (11 `false`, 2 `true`, **11 with the literal string `set this to true or false`**) | `pnpm-workspace.yaml:63-87` |
| `minimumReleaseAgeExclude` | **9** entries; `minimumReleaseAge: 4320` min = 72 h = 3 days | `pnpm-workspace.yaml:89-102` |
| Patches | **1** — `react-data-grid` | `pnpm-workspace.yaml:133-134`, `patches/react-data-grid.patch` |
| Lockfile | `lockfileVersion: '9.0'`, **1,373,478 bytes**, 38,614 lines, **3,472** `packages:` entries, **3,509** `snapshots:` entries, 29 importers | `pnpm-lock.yaml` |
| Workspace packages with a `build` script | **8** (the apps only — no `packages/*` has one) | measured over all 29 `package.json` |
| Workspace packages with `lint` / `typecheck` / `test` / `clean` | 7 / 17 / 14 / 23 | measured |
| Knip | **6.32.3**; `exclude: ["types","exports"]` → only files + deps gated | `package.json:66`, `knip.jsonc:5` |
| ESLint | `^9.0.0`; 2 custom rules; 3 `shadcn/*` rules at `warn` | `package.json:64`, `packages/eslint-config-supabase/next.js:55-56,79-81` |
| Prettier | `^3.8.0` | `package.json:67` |
| zizmor | **1.26.1** (pinned, binary downloaded + attestation-verified) | `.github/workflows/zizmor.yml:20,49-53` |
| ESLint ratchet baselines | studio **1,895** violations / 15 rules; www 851 / 3; design-system 72 / 3; docs 60 / 3; ui-library 49 / 3; learn 20 / 3 | `apps/*/.github/eslint-rule-baselines.json` |
| `ui-patterns` subpath export keys | **194** | `packages/ui-patterns/package.json:15` |
| Repo file count | 18,153 blobs (8,632 `.ts`/`.tsx`) | tree |
| Committed generated API types | `api-v1.d.ts` 367 KB, `api-v2.d.ts` 369 KB, `platform.d.ts` 960 KB, `fga-requirements.ts` 19 KB | `packages/api-types/types/` |

---

## How it works

### 1. Workspace layout

**Root manifest.** `package.json` is a private root with no runtime code, only scripts and tooling
(`package.json:1-7`). `preinstall` is `npx only-allow pnpm` (`package.json:9`) — npm/yarn are blocked
before install. 20 of the root scripts shell out to `turbo` (`package.json:10-35`; 21 total `turbo`
mentions in the file, the 21st being the pinned dependency at `package.json:74`).

**Workspace globs.** `pnpm-workspace.yaml:1-5`:

```yaml
packages:
  - apps/*
  - packages/*
  - blocks/*
  - e2e/*
```

Every directory under those four globs that owns a `package.json` becomes a workspace project. The
lockfile confirms exactly **29 importers** (root `.` plus 28 projects), and it matches the tree exactly —
no directory under `apps/`, `packages/`, `blocks/`, `e2e/` is missing a `package.json`.

Notably **not** workspaces: `examples/` (1,486 files of standalone sample apps, each with its own
`package-lock.json`/`yarn.lock`/`pnpm-lock.yaml` gitignored at `.gitignore:168-170`), `i18n/`, `supabase/`
(the local Docker project), `docker/`, `sitemaps/`. Those are content trees, not packages.

**How apps depend on packages.** Every internal dependency uses the pnpm `workspace:` protocol
(measured: 98 edges, zero version ranges without `workspace:`). Two shapes are used:

* `workspace:*` (94 edges) — pinned to the local package, never published.
* `workspace:^` (2 edges: `apps/learn` → `config`, `apps/ui-library` → `config`) and bare `workspace:`
  (2 edges: `packages/marketing` → `config`, `packages/shared-data` → `tsconfig`) — the latter means
  "any version of the local package".

**No build step for packages.** Packages publish TypeScript source, not compiled output:

* `packages/ui/package.json:4` → `"main": "./index.tsx"`, `:5` → `"types": "./index.tsx"`.
* `packages/api-types/package.json:5-6` → `main`/`types` = `./index.ts`.
* `packages/ui-patterns/package.json:15-…` → an `exports` map with **194** subpath entries, each
  `{"import": "./src/…", "types": "./src/…"}` (e.g. `"./Admonition/Admonition"` →
  `./src/Admonition/Admonition.tsx`). This is what makes `import { X } from 'ui-patterns/Admonition'` work
  in a bundler without a build.
* `packages/icons/package.json:2` → `"main": "./src/icons/index.ts"`.

Consequence: Next.js apps must transpile the raw TS from `node_modules`. Every Next app does this
explicitly:

* `apps/studio/next.config.ts:202` → `transpilePackages: ['ui','ui-patterns','common','shared-data','api-types','icons']`
* `apps/www/next.config.mjs:45-49`, `apps/docs/next.config.mjs:55-59` → same list + `dayjs`
* `apps/design-system/next.config.mjs:5`, `apps/ui-library/next.config.mjs:3` → `['ui','common','shared-data','icons','tsconfig']`

**Shared config package.** `packages/config` is the single source of Tailwind/PostCSS/theme truth:

* `packages/config/tailwind.config.css:1-42` — imports Tailwind v4, the two Tailwind plugins
  (`@tailwindcss/typography`, `@tailwindcss/forms`), the committed UI token sheets
  (`../ui/build/css/source/global.css`, `semantic.css`, `compat.css`, `themes/dark.css`, `themes/light.css`),
  and the local `css/*.css` layers.
* Apps consume it through PostCSS: `apps/studio/postcss.config.cjs:1` → `module.exports = require('config/postcss.config')`;
  `packages/config/postcss.config.js` registers `@tailwindcss/postcss`.
* `packages/ui/tailwind.config.css:1-4` is only a placeholder so the VS Code Tailwind extension finds the
  shared config — apps own the real entry CSS.

The `packages/ui/build/css/**` sheets (8 files) are **committed**, not generated — they are the
hand-maintained design-token source.

**Package-to-package graph (the interesting edges).**

* `packages/ui-patterns` → `packages/ui` (`workspace:*`) — composite patterns built on primitives.
* `packages/ui-patterns` → `packages/common`, `packages/icons`.
* `packages/common` → `packages/api-types`, `packages/config`.
* `packages/icons` → `packages/build-icons` (`@supabase/build-icons`) — the icon compiler.
* `apps/studio` → `packages/pg-meta` (`@supabase/pg-meta`) — safe SQL builders for introspection.
* `apps/www` → `packages/marketing`; `apps/ui-library` → `blocks/vue` (`@supabase/vue-blocks`).

### 2. Turborepo orchestration

**Root pipeline** (`turbo.jsonc:1-30`) defines 6 tasks:

| task | dependsOn | outputs | cache |
| --- | --- | --- | --- |
| `build` | `^build` | `dist/**`, `.next/**` (minus `.next/cache`, `.next/dev`) | on |
| `lint` | — | none | on |
| `clean` | — | none | **off** (`turbo.jsonc:15`), `outputLogs: errors-only` |
| `dev` | — | — | **off**, `persistent: true` (`turbo.jsonc:19-20`) |
| `test` | — | — | **off** (`turbo.jsonc:23`) |
| `typecheck` | `^typecheck` | none | on |

Plus `ui: "stream"` (`turbo.jsonc:3`) and `cacheMaxAge: "14d"` (`turbo.jsonc:4`).

**The `^build` graph is currently vacuous.** `dependsOn: ["^build"]` means "run `build` in my
*dependencies* first". But **no `packages/*` defines a `build` script** (measured: only the 8 apps do).
Every app still declares `dependsOn: ["^build"]` (`apps/studio/turbo.jsonc:6`, `apps/docs/turbo.jsonc:35`,
`apps/www/turbo.jsonc:20`, `apps/kb/turbo.jsonc:6`, `apps/learn/turbo.jsonc:6`,
`apps/lite-studio/turbo.jsonc:6`, `apps/design-system/turbo.jsonc:6`, `apps/ui-library/turbo.jsonc:6`) —
it is a leftover from when packages had build steps. The practical dependency ordering today comes from
pnpm's workspace links, not from Turbo.

**Per-app overrides.** All 8 apps have their own `turbo.jsonc` that `extends: ["//"]` (the root config)
and overrides `build`:

* `apps/studio/turbo.jsonc:7-126` — a **~90-entry `env` allow-list**. Turbo hashes these into the task
  hash, so changing e.g. `NEXT_PUBLIC_SUPABASE_URL` invalidates the cache. The list is annotated with
  the reason each var is there (`apps/studio/turbo.jsonc:111-115`: `MODE` selects the build flavour and
  *must* invalidate the cache, otherwise a test build reuses production output).
* `apps/studio/turbo.jsonc:127-135` — `passThroughEnv` for vars that must be forwarded but not hashed
  (`CURRENT_CLI_VERSION`, `VERCEL_GIT_COMMIT_REF`, S3 keys …).
* `apps/studio/turbo.jsonc:136-143` — outputs `.next/**`, `.output/**` (TanStack/Nitro),
  `.vercel/output/**`.
* `apps/docs/turbo.jsonc:5-29` — declares extra tasks: `codegen:examples`, `codegen:references`,
  `build:federated-content` (**`cache: false`** — "the inputs are remote, so a cache restore could
  resurrect stale content", `apps/docs/turbo.jsonc:14-15`), and `build:markdown` (which *does* declare
  `outputs: ["public/markdown/**", …]` so a cache hit still restores the generated markdown).
* `apps/docs/turbo.jsonc:35` — `build` dependsOn `["^build","codegen:examples","codegen:references","build:markdown"]`.
* `apps/www/turbo.jsonc:11-18` — `build` is `cache: false`, `dependsOn: []`, `outputs: []`,
  `passThroughEnv: ["*"]`. The cacheable task is `build:next` (`apps/www/turbo.jsonc:19-87`) with an
  explicit `inputs` list including `.env*`, `.generated/**`, `public/changelog/**`,
  `$TURBO_ROOT$/apps/docs/content/guides/**` and
  `$TURBO_ROOT$/apps/studio/components/ui/TwoOptionToggle.tsx` — i.e. www's Next compile is invalidated
  by a Studio component it imports.
* `apps/kb/turbo.jsonc:8` → `outputs: ["dist/**"]` (Astro); `apps/lite-studio/turbo.jsonc:10` →
  `outputs: ["build/**"]` (React Router).

**Nested Turbo.** `apps/www/package.json` `build` = `turbo run build:next --filter=www` — a Turbo
invocation *inside* a Turbo task. This is deliberate: `apps/www/turbo.jsonc:11-13` explains
"pnpm's prebuild refreshes remote content before the nested build:next run hashes it. postbuild uploads
assets on every deployment, including build:next cache hits." The outer task is uncached so the
`prebuild`/`postbuild` lifecycle always runs; the inner `build:next` is cached.

**Caching / remote cache.** Local caching is on (`.turbo` is gitignored, `.gitignore:17-18`).
**No remote cache is configured in the repo**: no `TURBO_TOKEN` / `TURBO_TEAM` / `remoteCache` key
appears in any of the 56 workflows or in any of the 9 `turbo.jsonc` files (measured by grep). The
`apps/www/turbo-build.test.ts` fixture explicitly writes `remoteCache: { enabled: false }`
(`apps/www/turbo-build.test.ts:60-63`) for its sandbox. Whether Vercel injects remote-cache credentials
into CI is not visible in the repository.

**Turbo behaviour is itself unit-tested.** `apps/www/turbo-build.test.ts` builds a throwaway pnpm
workspace with the *real* turbo binary (`apps/www/turbo-build.test.ts:161-165` symlinks
`node_modules/.bin/turbo`) and asserts the deployment ordering: `docs:fetch → docs:markdown →
www:content → compile → sitemap → upload:.next/static → upload:public`
(`apps/www/turbo-build.test.ts:198-206`), that a cache hit still uploads (`:210-220`), that changing
content / docs / env / a shared package / the imported Studio component invalidates the compile
(`:222-261`), and that a failure in an earlier stage prevents the upload (`:277-286`).

### 3. pnpm specifics

**Version and engines.** `packageManager: pnpm@11.13.1` (`package.json:88`), `engines.pnpm: "11.13"`,
`engines.node: ">=22.13"` (`package.json:83-86`), `.nvmrc` = `22` (`.nvmrc:1`).
`engineStrict: true` (`pnpm-workspace.yaml:8`) — a Node/pnpm mismatch is a hard install error.

**Settings** (`pnpm-workspace.yaml:7-11`):

* `blockExoticSubdeps: true` — no git/http/tarball sub-dependencies.
* `enableGlobalVirtualStore: false` — the virtual store stays inside the repo's `node_modules/.pnpm`
  rather than a global dir; the comment explains this is a TypeScript/peer-dep workaround
  (pnpm issue #9739). Practical effect: no cross-repo store sharing, bigger `node_modules`, but the
  store is disposable.
* `updateNotifier: false` — no version-check network call during install.

**Catalog.** 41 entries (`pnpm-workspace.yaml:13-61`). Version ranges are pinned in one place and
consumed as `catalog:` (e.g. `package.json:62-77`, `packages/ui/package.json` devDeps). The TypeScript
entry is unusual and worth knowing:

```yaml
# TypeScript 7 has no programmatic API until 7.1, so `typescript` stays aliased
# to the 6.0-API compat package for tools that import it (typescript-eslint,
# Next.js build typechecking), while `@typescript/native` provides the native
# TS 7 `tsc` binary used by typecheck scripts.
'@typescript/native': npm:typescript@~7.0.2
typescript: ~6.0.2
```
(`pnpm-workspace.yaml:28-33,56`)

**Overrides.** 24 entries (`pnpm-workspace.yaml:104-131`) — security pins (`tar`, `uuid`, `postcss`,
`dompurify`, `nodemailer`, `qs`), ecosystem pins (`monaco-editor`, `lodash`, `lodash-es`, `postcss` all
redirected to `catalog:`), and peer-dep dedupes (`h3@1` pinned to 1.15.11 so the Nuxt example does not
get two copies — `pnpm-workspace.yaml:115-118`).

**Supply-chain / release-age gate.** `minimumReleaseAge: 4320` minutes = 72 hours = 3 days
(`pnpm-workspace.yaml:89`) with 9 exclusions (`pnpm-workspace.yaml:91-102`: `@ai-sdk/*`, `@supabase/*`,
`typescript`, `@typescript/*`, `mdast-jsx`, plus 3 version-specific security exclusions).
`.github/dependabot.yml:9-27` documents the coupling: Dependabot gets a **4-day cooldown** because
"its PRs are structurally guaranteed to fail CI/Vercel" otherwise.

**Build-script allow-list (`allowBuilds`).** 24 entries (`pnpm-workspace.yaml:63-87`): 11 explicit
`false` (blocking install scripts of `@parcel/watcher`, `@sentry/cli`, `contentlayer2`, `core-js`,
`esbuild`, `es5-ext`, `libpg-query`, `msgpackr-extract`, `msw`, `protobufjs`, `sharp`), 2 `true`
(`node-pty`, `supabase`), and **11 with the literal placeholder string `set this to true or false`**
for the `file:`-linked workspace packages (`packages/build-icons`, `packages/pg-meta`,
`packages/ai-commands`, `packages/api-types`, `packages/common`, `packages/config`,
`packages/dev-tools`, `packages/icons`, `packages/shared-data`, `packages/ui-patterns`, `packages/ui`).

**Patches.** Exactly one: `react-data-grid` → `patches/react-data-grid.patch`
(`pnpm-workspace.yaml:133-134`). The patch rewrites `onLostPointerCapture` in `lib/bundle.cjs` and
`lib/bundle.js` so a lost pointer capture no longer fires `onPointerMove` — a column-resize fix.

**Lockfile.** `lockfileVersion: '9.0'`, `autoInstallPeers: true`, `excludeLinksFromLockfile: false`
(`pnpm-lock.yaml:1-5`). 1.37 MB, 38,614 lines, 3,472 package entries, 3,509 snapshot entries, 29
importers. `settings.autoInstallPeers: true` means peer deps are auto-installed rather than warned about.

**Install speed notes (measured locally, not from the repo).** I installed pnpm 11.13.1 on this box and
ran controlled experiments:

| Behaviour | Measured result |
| --- | --- |
| `pnpm install --frozen-lockfile` | works in 11.13.1 (exit 0). pnpm 11 makes frozen-lockfile the **default in CI** ("in CI environments this setting is true by default"). |
| `allowBuilds: { <pkg>: false }` | install **succeeds** (exit 0); the package's install script is silently skipped. |
| `allowBuilds: { <pkg>: <non-boolean string> }` | install **FAILS**: exit 1, `[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@0.28.2`. |
| `allowBuilds` key `esbuild@0.28.2` | matches → script blocked, exit 0. |
| `allowBuilds` key `esbuild@file:packages/esbuild` | does **not** match a registry install → script "not decided" → exit 1. |
| Workspace `file:` project with a `postinstall` | always runs, regardless of the `allowBuilds` value. |
| `minimumReleaseAge: 999999` | install **FAILS**: exit 1, `[ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION] 27 lockfile entries failed verification`. |

Install cost drivers visible in the config: 3,472 resolved packages, one patch, 24 overrides,
a 3-day release-age gate, and `enableGlobalVirtualStore: false` (no cross-project store reuse).

### 4. CI

**56 workflow files** in `.github/workflows/`, **28** of them PR-triggered. The always-on PR gates:

| Workflow file | Trigger | What it does | Fails on |
| --- | --- | --- | --- |
| `validate-pr.yml` | `pull_request` (no branch filter) | Fails if the PR carries the `do-not-merge` label (`:14-18`) | label present |
| `typecheck.yml` | `pull_request` → `master`, and `merge_group` | Runs `node scripts/check-case-hazards.mjs` **before install** (`:40-44`), then `pnpm run typecheck` and `pnpm run lint` **in parallel** (`:51-58`) | any type error, any lint error, any case hazard |
| `prettier.yml` | `pull_request` → `master` | `pnpm run test:prettier` (`:43-45`) | any formatting diff |
| `avoid-typos.yml` | `pull_request` (opened/synchronize/reopened/edited) | `reviewdog/action-misspell` with `locale: US`, `reporter: github-pr-review`, `level: error` (`:23-29`) | **reviewdog comments only — see gotcha #1** |

`typecheck.yml` uses `blacksmith-4vcpu-ubuntu-2404` runners and `NODE_OPTIONS: --max-old-space-size=4096`
(`:19-21`). Most other workflows use the same runner; `validate-pr.yml` and
`eslint-config-supabase-tests.yml` use plain `ubuntu-latest`.

**Path-filtered PR workflows** (run only when the relevant files change):

| Workflow | Path filter | Command |
| --- | --- | --- |
| `studio-knip.yml` | `apps/studio/**`, `knip.jsonc`, `package.json`, `pnpm-lock.yaml`, `pnpm-workspace.yaml` | `pnpm knip --workspace apps/studio --no-progress --reporter symbols --reporter github-actions` (`:64-65`) |
| `studio-unit-tests.yml` | `apps/studio/**`, `packages/ui/**`, `packages/ui-patterns/**`, `packages/common/sentry.ts` | `pnpm run test:ci` in `apps/studio` (`:76-82`), then Coveralls upload |
| `studio-lint-ratchet.yml` | `apps/studio/**`, `packages/**`, `pnpm-lock.yaml` | `pnpm --filter studio run lint:ratchet` (`:48-49`) |
| `lint-ratchet.yml` | per-app matrix: `www`, `docs`, `design-system`, `ui-library`, `learn` + `packages/**` + `pnpm-lock.yaml` | `pnpm --filter "./apps/$APP" run lint:ratchet` (`:82-85`) |
| `library-tests.yml` | `packages/ui`, `ui-patterns`, `common`, `icons`, `shared-data`, `api-types`, `config`, `tsconfig`, `eslint-config-supabase`, `patches`, `apps/ui-library`, `blocks/vue` | `pnpm --filter library test`, `build:registry`, then a **generated-file diff check** (`:52-59`), then `build` |
| `ui-tests.yml` / `ui-patterns-tests.yml` | `packages/ui/**` / `packages/ui-patterns/**` | vitest; ui-patterns also regenerates `package.json` exports and fails if it changed (`:43-48`) |
| `www-tests.yml` / `docs-tests.yml` | app paths | vitest in `apps/www` / `apps/docs` |
| `eslint-config-supabase-tests.yml` | `packages/eslint-config-supabase/**` | `pnpm --filter eslint-config-supabase run test` |
| `verify-production-api-types.yml` | PR touches `packages/api-types/(types\|scripts)/` | `pnpm --filter=api-types run verify-production-types` (`:48-50`) |
| `zizmor.yml` | `.github/workflows/**`, `zizmor.yml` | `zizmor --config zizmor.yml .github/workflows` (`:55-58`) |
| `pg-meta-tests.yml`, `docs-e2e.yml`, `www-e2e.yml`, `studio-e2e-test.yml`, `ai-tests.yml`, `self-host-tests-smoke.yml`, `studio-docker-build.yml`, `braintrust-*` | various | app-specific suites |

**Non-PR automation** (28 workflows): `autofix_linters.yml` (on the `autofix` label, runs
`pnpm run format` and pushes a patch via a GitHub App — `autofix_linters.yml:50-52,104-118`),
`fix-typos.yml` (weekly on master, opens a PR with `misspell-fixer-action`),
`lint-ratchet-decrease.yml` (weekly cron `0 0 * * SUN`, lowers the baselines and opens a bot PR —
`lint-ratchet-decrease.yml:74-76`, `:97-101`), `studio-lint-ratchet-decrease.yml`, `docs-sync.yml`,
`update-js-libs.yml`, `publish_image.yml`, `refresh-sitemaps.yml`, `stale.yml`, `label_prs.yml`, etc.
**zizmor** is a GitHub Actions security scanner (pin-to-SHA hardening, template injection, …). It is
pinned to `1.26.1`, the binary is downloaded from GitHub releases and **attestation-verified** with
`gh attestation verify` before use (`.github/workflows/zizmor.yml:42-53`). Four workflows are exempted
from the `dangerous-triggers` rule: `authorize-vercel-deploys.yml`, `external-pr-comment.yml`,
`label_prs.yml`, `studio-master-alert.yml` (`zizmor.yml:1-7`).

### 5. Code quality tooling

**ESLint 9 flat config.** The shared preset lives in `packages/eslint-config-supabase/next.js`
(`main: "next.js"`, `packages/eslint-config-supabase/package.json:4`). It composes:

* `eslint-config-turbo/flat` and `eslint-config-prettier/flat` (`next.js:3-4`, `:67-68`) — prettier
  turns off formatting rules; turbo turns off the "no undeclared env vars" rule.
* `@shadcn/lint` with `componentImports: ['^ui(/|$)', '^ui-patterns(/|$)']` (`next.js:73-76`), and
  three rules at **`warn`**: `shadcn/no-unknown-classes`, `shadcn/no-arbitrary-values`,
  `shadcn/no-raw-colors` (`next.js:78-82`).
* `@tanstack/eslint-plugin-query` recommended + `exhaustive-deps: warn` (`next.js:84-89`).
* `eslint-config-next/core-web-vitals` (`next.js:91`) with all React Compiler hook rules turned off
  except `exhaustive-deps` and `rules-of-hooks` (`next.js:18-29`).
* Two **custom Supabase rules at `error`**: `supabase/no-await-before-copy-to-clipboard` and
  `supabase/require-explicit-tabindex` (`next.js:32-37`, `:55-56`; implementations in
  `packages/eslint-config-supabase/rules/`).
* `no-restricted-exports` at `warn` — default exports are banned except in `pages/**`, `app/**`,
  a few config files (`next.js:114-137`).
* `no-restricted-imports` at `warn` — `react-data-grid` and `react-contexify` are banned in favour of
  `@tanstack/react-table` and the `ui` package (`next.js:101-111`).
* `.mts`/`.cts` are globally ignored (`next.js:66`).

Each app adds its own `eslint.config.cjs` that pulls in the shared preset:
`apps/studio/eslint.config.cjs:9`, `apps/www/eslint.config.cjs:2`, `apps/docs/eslint.config.cjs:2`,
`apps/learn/eslint.config.cjs:2`, `apps/design-system/eslint.config.cjs`, `apps/ui-library/eslint.config.cjs`.
Studio layers on `eslint-plugin-barrel-files`, `eslint-plugin-valtio`, `eslint-plugin-react-hook-form`
(shimmed for ESLint 9 via `fixupPluginRules`) and ~20 `no-restricted-syntax` rules
(`apps/studio/eslint.config.cjs:1-8`, `:14-70`). `apps/www` adds a local rule
`www/no-cross-zone-link` at `error` (`apps/www/eslint.config.cjs:24-28`).

**Important: `lint` scripts do not fail on warnings.** Every `lint` script is a bare `eslint .`
(no `--max-warnings`). ESLint exits 0 when there are only warnings. That is exactly why the ratchet
exists.

**The lint ratchet** (`packages/eslint-config-supabase/ratchet-eslint-rules.ts`) is the real lint gate:

* It runs ESLint with `--format json` (`ratchet-eslint-rules.ts:167-175`) and counts occurrences of the
  selected rules, *ignoring test files* (`ratchet-eslint-rules.ts:288`).
* It compares against a committed baseline (default `.github/eslint-rule-baselines.json`,
  `ratchet-eslint-rules.ts:107`) and **exits 1 if any rule's current count exceeds the baseline**
  (`ratchet-eslint-rules.ts:350-369`, `:404-407`), printing
  `::error title=New violations::You added N new violations of <rule>`.
* It exits **2** if a rule has no baseline at all (`ratchet-eslint-rules.ts:325-332`).
* `--decrease-baselines` lowers the stored baseline when the count improves
  (`ratchet-eslint-rules.ts:370-375`, `:388-400`); the weekly cron job uses it.
* It stores both a total and a **per-file breakdown** (`ratchet-eslint-rules.ts:70-78`, `:247-266`),
  so the error message names the offending files (`ratchet-eslint-rules.ts:429-459`).

Rule sets: studio uses 12 studio rules (`apps/studio/scripts/ratchet-rules.json`) plus the 3 shared
`shadcn/*` rules (`packages/eslint-config-supabase/ratchet-rules.json`) = **15 rules, 1,895 baseline
violations**; the other five apps use only the 3 shared rules (www 851, design-system 72, docs 60,
ui-library 49, learn 20).

**Prettier** (`prettier.config.mjs`): `printWidth: 100`, `semi: false`, `singleQuote: true`,
`trailingComma: 'es5'`, `tabWidth: 2`, `endOfLine: 'lf'`, plus `prettier-plugin-sql-cst` for SQL
(`prettier.config.mjs:1-18`). Import sorting via `@ianvs/prettier-plugin-sort-imports` with
`importOrder: ['<THIRD_PARTY_MODULES>', '', '^(@|\\.{1,2})/(.*)$']` (`prettier.config.mjs:20-23`).

The `SORT_IMPORTS` env var is the switch: in CI the root scripts set `SORT_IMPORTS=false`
(`package.json:28-29`), which **disables import sorting globally but keeps it for
`apps/studio/**/*.{js,jsx,ts,tsx}`** via a config override (`prettier.config.mjs:27-34`). So Studio files
must be import-sorted; everything else must not be re-sorted (otherwise CI and the editor fight).

The checked glob is `'{apps,packages,blocks,examples,i18n}/**/*.{js,jsx,ts,tsx,css,md,mdx,json}'`
(`package.json:28`) — note `e2e/`, `scripts/`, `supabase/` and `docker/` are **not** prettier-checked, and
`.astro` files are not covered either.

`.prettierignore` (42 lines) excludes build output, generated trees
(`apps/docs/**/generated/*`, `apps/docs/__generated__`, `apps/www/.generated/*`,
`apps/www/components/Partners/__generated__`, `apps/design-system/__registry__`,
`packages/icons/__registry__`, `packages/icons/src/icons/*.ts`, `apps/ui-library/__registry__`,
`apps/studio/routeTree.gen.ts`) and SQL that prettier-plugin-sql-cst cannot parse
(`.prettierignore:8-11`).

**Knip** (unused-export / unused-file / unused-dependency detection), version **6.32.3**
(`package.json:66`). Config `knip.jsonc`:

* `exclude: ["types","exports"]` (`knip.jsonc:5`) — only **files and dependencies** are gated; the
  export/type surface is deliberately not enforced ("the export/type surface has too much noise").
* `ignore` for `examples/**`, `**/*.mdx`, `supabase/functions/**`, `**/*.test.ts`, the ui-library
  registry (`knip.jsonc:6-15`).
* A workspace block for `apps/studio` with `entry` (TanStack `router.tsx`, `start.ts`, `routes/**`,
  `compat/**`) so knip traces them (`knip.jsonc:23-39`), `ignore` for one-off scripts and dynamic
  imports (`knip.jsonc:40-51`), narrowly scoped `ignoreIssues` for 4 specific files
  (`knip.jsonc:57-74`), and `ignoreDependencies` for 5 packages that are needed but not importable
  (`knip.jsonc:80-94`).

The root `package.json` exposes `pnpm knip` (`package.json:56`); CI runs it scoped to studio
(`studio-knip.yml:64-65`). Knip **does** exit non-zero on findings, so `studio-knip.yml` is a real
blocking check on PRs touching `apps/studio/**`.

**misspell / misspell-fixer.** Two different tools:

* `avoid-typos.yml` — PR-time `reviewdog/action-misspell` with `locale: US`, `reporter:
  github-pr-review`, `level: error`, excluding `*.css`, `**/package.json`, `**/pnpm-lock.yaml`,
  `*.ipynb`, `./i18n/README.*.md`, `./studio/public/monaco-editor/*` (`avoid-typos.yml:23-37`).
* `fix-typos.yml` — weekly on master, `sobolevn/misspell-fixer-action@0.1.0` + a bot PR
  (`fix-typos.yml:24-38`). Ignore list: `./i18n`, `./packages/api-types`,
  `./apps/www/lib/redirects.js`, `./apps/studio/public/*` (`.misspell-fixer.ignore:1-4`).

**zizmor** — GitHub Actions security scanner, see §4.

**CodeRabbit** (`.coderabbit.yaml`, 153 lines): `inheritance: false` so org settings do not leak in
(`:5`); `path_filters` skip machine-generated files (`!pnpm-lock.yaml`, `!packages/api-types/types/**`,
`!supabase/functions/common/database-types.ts`, `!**/routeTree.gen.ts`, `!**/__generated__/**`, …)
(`:17-29`); path-scoped `path_instructions` for telemetry naming (`packages/common/telemetry-constants.ts`),
Studio PostHog tracking, the Next↔TanStack route mirror, docs style, and an a11y checklist
(`:32-132`); `knowledge_base.code_guidelines` points CodeRabbit at `.agents/skills/*/SKILL.md` with an
explicit `applyTo` because the skills live outside the code they govern (`:134-153`).
CodeRabbit is advisory — it posts review comments, it is not a CI gate.

**Which of these actually fail CI?** Failing: `typecheck.yml` (typecheck, lint, case hazards),
`prettier.yml`, `validate-pr.yml` (label), `studio-knip.yml`, `studio-lint-ratchet.yml`,
`lint-ratchet.yml`, `library-tests.yml` (incl. the generated-registry diff check), the app test suites,
`eslint-config-supabase-tests.yml`, `verify-production-api-types.yml`, `zizmor.yml`.
Non-failing (advisory): `avoid-typos.yml` (reviewdog `fail_level` defaults to `none`), CodeRabbit,
`autofix_linters.yml` (it opens a patch, it does not gate).

### 6. TypeScript setup

**The root `tsconfig.json` is almost empty** — only `jsx: "react"` and `skipLibCheck: true`
(`tsconfig.json:1-6`). It is not a `base` that apps extend.

**The real base lives in `packages/tsconfig`** (`packages/tsconfig/package.json:6` ships
`base.json`, `nextjs.json`, `react-library.json`):

* `packages/tsconfig/base.json:4-19` — `strict: true`, `isolatedModules: true`, `declaration: true`,
  `declarationMap: true`, `esModuleInterop: true`, `forceConsistentCasingInFileNames: true`,
  `incremental: true`, `resolveJsonModule: true`, `noUnusedLocals: false`,
  `noUnusedParameters: false`.
* `packages/tsconfig/nextjs.json:4-13` — extends base; `noEmit: true`, `jsx: preserve`,
  `module: preserve`, `target: ES2021`.
* `packages/tsconfig/react-library.json:4-10` — extends base; `jsx: react-jsx`,
  `module: preserve`, `moduleResolution: bundler`, `target: es2021`.

**How packages share types.** They extend the shared config by package name (resolved through the pnpm
workspace link, i.e. `node_modules/tsconfig` → `packages/tsconfig`):

* `packages/ui/tsconfig.json:2`, `packages/common/tsconfig.json:2`, `packages/icons/tsconfig.json:2`,
  `packages/ui-patterns/tsconfig.json:2`, `packages/marketing/tsconfig.json:2`,
  `packages/shared-data/tsconfig.json:2`, `packages/ai-commands/tsconfig.json:2`,
  `packages/docs-search/tsconfig.json:2`, `packages/dev-tools/tsconfig.json:2` → `tsconfig/react-library.json`
* `packages/generator/tsconfig.json:2` → `tsconfig/base.json`
* `packages/pg-meta/tsconfig.json:2` → `../tsconfig/base.json` (relative path, because the package name
  is `@supabase/pg-meta` and the bare `tsconfig` specifier would be ambiguous)
* `apps/studio/tsconfig.json:4`, `apps/docs/tsconfig.json:4`, `apps/www/tsconfig.json:4`,
  `apps/ui-library/tsconfig.json:4`, `apps/design-system/tsconfig.json:4`, `apps/learn/tsconfig.json:4`,
  `apps/lite-studio/tsconfig.json:4`, `blocks/vue/tsconfig.json:2` → `tsconfig/nextjs.json`
* `apps/kb/tsconfig.json:2` → `astro/tsconfigs/strict` (Astro's own preset, not the shared one)

**Path aliases** are per-app and all point at the app root:

* `apps/studio/tsconfig.json:9-11` → `"@/*": ["./*"]`
* `apps/docs/tsconfig.json:7-11` → `"~/*": ["./*"]` (deprecated) + `"@/*": ["./*"]`
* `apps/www/tsconfig.json:7-40` → a large legacy alias table (`~/*`, `app/*`, `components/*`, `data/*`,
  `hooks/*`, `internals/*`, `layouts/*`, `lib/*`, `pages/*`, `public/*`, `scripts/*`, `styles/*`, `types*`)
  each marked `@deprecated: use @/ prefix instead`, plus `contentlayer/generated` and `.generated/*`.
* `apps/design-system/tsconfig.json:8-11` → `@/*` plus `icons/*` → `./../../packages/icons/*`
* `apps/learn/tsconfig.json:5-9` → `"*": ["./*"]` and `"@/*": ["./*"]`
* `apps/lite-studio/tsconfig.json:6-8` → `"@/*": ["./app/*"]`
* `blocks/vue/tsconfig.json:4-6` → `@/*`

**Typecheck is a separate Turbo task**, `dependsOn: ["^typecheck"]` (`turbo.jsonc:25-28`), run by
`turbo --continue typecheck` (`package.json:26`) so every workspace reports even after one fails.
Three apps need a codegen step first via the `pretypecheck` hook: `apps/docs` (`pretypecheck` =
`pnpm run codegen:graphql && next typegen`), `apps/studio` (`next typegen`), `apps/www`
(`next typegen`) — `apps/studio/package.json`, `apps/docs/package.json`, `apps/www/package.json`.

**Cross-package type sharing** is done through the workspace source, not through build artifacts:
`packages/api-types/index.ts` re-exports and *merges* the three generated OpenAPI type sets into one
`paths` / `operations` / `components` interface (`packages/api-types/index.ts:19-35`) and every consumer
imports `api-types` as a devDependency.

**`@typescript/native`** is the actual `tsc` used by the `typecheck` scripts
(`packages/tsconfig/base.json` is the config; the binary comes from the `@typescript/native` catalog
alias to TypeScript 7). The catalog comment (`pnpm-workspace.yaml:28-33`) explains the split:
`typescript` stays at the 6.0 API for tools that import the TS API (typescript-eslint, Next's build
typecheck), while `@typescript/native` gives the native TS 7 `tsc` binary.

### 7. Generated code

**`packages/api-types` — the platform Management API types. Committed.**

* Sources: three OpenAPI specs. `packages/api-types/redocly.yaml:1-14` points at a **local** API
  (`http://localhost:8080/api/{v1-json,v2-json,platform-json}`); the production variant
  (`packages/api-types/scripts/verify-production-types.mjs:19-23`) points at
  `https://api.supabase.com/api/{v1-json,v2-json,platform-json}`.
* `pnpm api:codegen` → `cd packages/api-types && pnpm run codegen` (`package.json:53`) →
  `openapi-typescript --redocly ./redocly.yaml --alphabetize --default-non-nullable=false` then
  `node ./scripts/generate-fga-requirements.mjs` then prettier
  (`packages/api-types/package.json:10`).
* `pnpm api:codegen:prod` → `pnpm --filter=api-types run codegen:prod` (`package.json:54`) →
  `node ./scripts/generate-production-types.mjs` (`packages/api-types/package.json:11`) which
  regenerates the committed files **directly from production**, no local API needed
  (`packages/api-types/scripts/generate-production-types.mjs:11-24`).
* Outputs (committed, in the repo tree): `packages/api-types/types/api-v1.d.ts` (367,357 B),
  `api-v2.d.ts` (368,817 B), `platform.d.ts` (959,888 B), `fga-requirements.ts` (19,329 B).
* **CI enforces that the committed files match production**: `pnpm api:verify-types`
  (`package.json:55`) → `verify-production-types.mjs` fetches the three specs into a temp dir, runs
  `openapi-typescript` there, and diffs against the committed files
  (`packages/api-types/scripts/verify-production-types.mjs:195-215`); a mismatch throws
  `Committed API types do not match production: …` and writes a markdown diff into
  `$GITHUB_STEP_SUMMARY` (`:73-121`). `verify-production-api-types.yml` runs it whenever the PR touches
  `packages/api-types/(types|scripts)/` (`:19-23`, `:48-50`).
* Note the explicit Prettier-config plumbing: the generated files live in a temp dir outside the repo, so
  the script resolves the repo's Prettier config path explicitly
  (`packages/api-types/scripts/verify-production-types.mjs:171-192`) — otherwise Prettier defaults would
  make every diff noisy.

**Other generated artefacts (committed, and marked as never-hand-edit in `AGENTS.md:47`):**

* `supabase/functions/common/database-types.ts` — `pnpm generate:types` runs
  `supabase gen types typescript --local > ./supabase/functions/common/database-types.ts`
  (`package.json:52`).
* `packages/api-types/types/**` — above.
* `**/routeTree.gen.ts` — TanStack Router (e.g. `apps/studio/routeTree.gen.ts`).
* `**/__generated__/**` — `apps/www/components/Partners/__generated__`, `apps/docs/__generated__`.
* `apps/docs/features/docs/generated/**` — docs reference markdown, built by
  `apps/docs` `codegen:references` (`apps/docs/package.json`).
* `apps/www/.generated/**` — static content, built by `apps/www` `content:build:core`
  (`scripts/generateStaticContent.mjs`, `scripts/generateMdContent.mjs`).
* `packages/icons/src/icons/*.ts` and `packages/icons/__registry__/**` — the icon compiler
  (`packages/icons/package.json` `build:icons` → `build-icons --templateSrc=…`).
* `apps/design-system/__registry__`, `apps/ui-library/__registry__`, `apps/ui-library/public/r/**` —
  shadcn registries; the `library-tests.yml` workflow fails if the committed registry does not match a
  fresh `pnpm --filter library build:registry` (`.github/workflows/library-tests.yml:52-59`).
* `apps/docs/public/markdown/**` — the guide markdown + `manifest.json`
  (`apps/docs/turbo.jsonc:26-29`).
* `apps/docs/content/_partials/access-control/scoped_pat_*.mdx` — built by
  `make -C apps/docs/spec generate.partials.access-control` (`AGENTS.md:47`).

**`packages/build-icons`** is the icon compiler itself: `packages/build-icons/src/main.mjs` reads
`src/raw-icons`, renders SVGs, and emits per-icon files, an aliases file, dynamic imports and an
exports file (`:41-96`). It is consumed by `packages/icons` (`@supabase/build-icons`), which wires it
with a template: `build-icons --templateSrc=./scripts/exportTemplate.mjs --renderUniqueKey
--iconFileExtension=.ts --exportFileName=index.ts` (`packages/icons/package.json`).

**`packages/generator`** is a small tsdoc helper (not a code generator for the monorepo):
`@supabase/generator` runs `tsx ./tsdoc.ts --input … --output …` to dereference TSDoc for 12 API
surfaces (v1 + v2 × functions/gotrue/postgrest/realtime/storage/supabase) into
`apps/docs/spec/enrichments/tsdoc_*/ *_dereferenced.json` (`packages/generator/package.json`).

---

## Failure modes / gotchas

### Gotcha 1 — The typos check does not fail the build

**Symptom:** you introduce "recieve" in a source file, push, and `avoid-typos.yml` goes green. You only
find out because a reviewer sees the inline comment.

**Why:** `reviewdog/action-misspell` is pinned at `ba7ac40` (`avoid-typos.yml:24`). Its `action.yml`
declares `fail_level` with default **`none`** ("always use exit code 0 for reviewdog") and
`fail_on_error` default `false` (deprecated in favour of `fail_level`). The workflow sets neither — it
only sets `level: error`, which is the *report* severity for annotations, not the failure threshold
(`avoid-typos.yml:23-29`). So the job always exits 0.

This contradicts `AGENTS.md:45` ("Every PR must pass typecheck + lint (one workflow), Prettier, and a
typos check"). The typos gate is advisory. Fixing it means adding `fail_level: error` to the step.

### Gotcha 2 — `allowBuilds` with a non-boolean value breaks `pnpm install`

**Symptom:** `pnpm install` (and therefore every CI job) dies with
`[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: <pkg>@<version>` and exit code 1 — with no obvious
connection to the change you made.

**Why:** `pnpm-workspace.yaml:63-87` contains **11 entries whose value is the literal string
`set this to true or false`** instead of `true`/`false`. I measured pnpm 11.13.1 behaviour directly:

* `allowBuilds: { <pkg>: false }` → install **succeeds** (exit 0); the install script is silently skipped.
* `allowBuilds: { <pkg>: "set this to true or false" }` → install **fails**, exit 1,
  `[ERR_PNPM_IGNORED_BUILDS]`.
* `allowBuilds` keys are matched against `name@resolvedVersion`; the `name@file:path` form used in the
  repo does **not** match a registry install (so a key like `esbuild@file:packages/esbuild` leaves the
  decision "unmade" → error).
* Workspace `file:` projects are exempt: their `postinstall` runs regardless of the `allowBuilds` value.

Today the repo survives only because those 11 keys point at workspace projects (which are never
install-script-gated). The moment one of those packages gains a registry dependency with an install
script — or the key format is "tidied" — the install breaks. The fix is to replace the placeholders with
real booleans.

### Gotcha 3 — `minimumReleaseAge` (3 days) makes fresh dependency versions uninstallable

**Symptom:** `pnpm install` fails with `[ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION] N lockfile entries
failed verification` right after a dependency was published (or after Dependabot proposes it).

**Why:** `pnpm-workspace.yaml:89` sets `minimumReleaseAge: 4320` (72 hours). I reproduced the failure
locally with pnpm 11.13.1 (exit 1, `[ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION]`). Nine exclusions
(`pnpm-workspace.yaml:91-102`) carve out `@ai-sdk/*`, `@supabase/*`, `typescript`, `@typescript/*`,
`mdast-jsx` and three pinned versions.

This is also why `.github/dependabot.yml:9-27` gives Dependabot a 4-day cooldown: without it,
"Dependabot's PRs are structurally guaranteed to fail CI/Vercel until the proposed version happens to
age past the pnpm gate on its own".

### Gotcha 4 — The case-sensitivity gate is the only thing that catches macOS/Windows breakage

**Symptom:** on a case-insensitive filesystem (macOS, Windows) a module silently exports nothing, or one
file clobbers another on clone. On CI (Linux, case-sensitive) everything passes.

**Why:** `scripts/check-case-hazards.mjs` exists precisely for this. Its header
(`scripts/check-case-hazards.mjs:3-19`) explains two failure modes: a self-resolving import
(`./Admonition` inside `admonition.tsx` resolves to the *directory* on Linux, but on a case-insensitive
filesystem the bundler lands back on the importing file, "The module then re-exports itself and
silently exports nothing"), and two tracked paths that differ only by case (one silently clobbers the
other on clone). It is run **before `pnpm install`** in `typecheck.yml:43-44` because it needs no
dependencies and fails fast. It exits 1 with a `❌` report (`scripts/check-case-hazards.mjs:153-170`).

Two escape hatches to know: `IGNORED_SEGMENTS = ['node_modules', '__generated__', '.generated']`
(`scripts/check-case-hazards.mjs:31`) and the fact that a specifier with an explicit extension is never
at risk (`scripts/check-case-hazards.mjs:77-80`, `:93`).

### Gotcha 5 — Turbo cache staleness in `apps/www`

**Symptom:** `pnpm build:www` reports "cache hit" and skips `next build`, but the deployed site has
stale content, or a Studio component change does not show up on www.

**Why:** www's cacheable task is `build:next`, whose `inputs` list is a hand-maintained allow-list
(`apps/www/turbo.jsonc:21-36`) — it includes `.env*`, `.generated/**`, `public/changelog/**`,
`$TURBO_ROOT$/apps/docs/content/guides/**` and
`$TURBO_ROOT$/apps/studio/components/ui/TwoOptionToggle.tsx`. Anything the Next compile reads that is
not in that list is **not** part of the cache key. The outer `build` task is `cache: false` with
`dependsOn: []` and `outputs: []` (`apps/www/turbo.jsonc:11-18`), so the outer turbo never restores
anything; only the inner nested `turbo run build:next` caches
(`apps/www/package.json` `build` script). Adding a new cross-package file that www imports requires
adding it to that `inputs` list.

The repo has a regression test for exactly this class of bug:
`apps/www/turbo-build.test.ts:222-261` asserts that changing the generated content, the docs markdown,
the agent-skills file, a `NEXT_PUBLIC_*` env var, `VERCEL_GIT_COMMIT_SHA`, the shared `packages/common`
package, or `apps/studio/components/ui/TwoOptionToggle.tsx` each invalidates the compile.

### Gotcha 6 — ESLint warnings never fail; only the ratchet does

**Symptom:** you add a `shadcn/no-arbitrary-values` warning (e.g. `p-[13px]`) in `apps/www` and the
"Rechtes studio lint checks" / "Ratchet lint checks" job fails with
`::error title=New violations::You added a new violation of shadcn/no-arbitrary-values`. But the *same*
class of change in `packages/ui` passes silently, because no ratchet baseline exists for that
workspace.

**Why:** `lint` scripts are bare `eslint .` with no `--max-warnings` (e.g. `apps/www/package.json`),
and ESLint exits 0 on warnings. The three `shadcn/*` rules are `warn` in the shared preset
(`packages/eslint-config-supabase/next.js:78-82`). The real gate is the ratchet
(`packages/eslint-config-supabase/ratchet-eslint-rules.ts:350-369`): it fails only if the **count** of
violations for a ratcheted rule rises above the committed baseline. Baselines live per app in
`apps/<app>/.github/eslint-rule-baselines.json` (studio: 1,895 across 15 rules; www: 851 across 3).
Test files are excluded from the count (`ratchet-eslint-rules.ts:288`), so adding a `.test.ts` with 50
violations will not trip the ratchet — but moving them into a non-test file will.

Corollary: a rule that is *not* in the ratchet set is effectively un-gated. `packages/ui`,
`packages/ui-patterns`, `apps/kb`, `apps/lite-studio` and `apps/studio`'s non-`shadcn` rules have no
baseline at all.

### Gotcha 7 — `pnpm test:prettier` does not check `e2e/`, `scripts/`, `supabase/`, `docker/` or `.astro`

**Symptom:** you format a file under `e2e/` or `scripts/` with your editor's Prettier and nothing
changes in CI; conversely a Prettier upgrade that reformats `e2e/` files produces a diff that CI never
complains about but that reviewers see.

**Why:** the glob is `'{apps,packages,blocks,examples,i18n}/**/*.{js,jsx,ts,tsx,css,md,mdx,json}'`
(`package.json:28`) and `.prettierignore` has no entry for those trees. The CI workflow also
sparse-checks-out only `apps`, `blocks`, `examples`, `i18n`, `packages`, `patches`
(`.github/workflows/prettier.yml:24-30`) — so the two agree, and the omissions are silent.

Also note the import-sorting asymmetry: CI sets `SORT_IMPORTS=false` globally but Studio files are still
sorted (`prettier.config.mjs:27-34`). If you sort imports in `apps/docs` by hand, CI will *not* complain,
but Studio files with unsorted imports **will** fail.

### Gotcha 8 — `apps/www` has a nested Turbo invocation

**Symptom:** `turbo run build` at the repo root and `pnpm build` inside `apps/www` produce different
task graphs; a cache hit in one does not imply a cache hit in the other; `turbo run build --filter=www`
from the root does not behave like the app's own build script.

**Why:** `apps/www/package.json` `build` = `turbo run build:next --filter=www` — Turbo inside Turbo.
The outer `build` task is `cache: false`, `dependsOn: []`, `outputs: []`, `passThroughEnv: ["*"]`
(`apps/www/turbo.jsonc:11-18`) so the `prebuild`/`postbuild` lifecycle always runs; only `build:next`
is cacheable (`apps/www/turbo.jsonc:19-87`). `apps/www/turbo-build.test.ts:263-275` asserts that the
root-level Turbo build and the app-level build produce the same content refresh + upload sequence.

---

## When to use this / when not to

**Use this build system when:**

* You are changing **app-level** code (`apps/studio`, `apps/docs`, `apps/www`, `apps/kb`,
  `apps/design-system`, `apps/ui-library`, `apps/learn`, `apps/lite-studio`) and want the CI gate list
  that applies to your paths.
* You are changing a **shared package** (`packages/ui`, `packages/ui-patterns`, `packages/common`,
  `packages/icons`, `packages/api-types`, `packages/config`, `packages/shared-data`) and need to know
  which downstream apps must re-lint/re-test — `library-tests.yml` and `studio-unit-tests.yml` are the
  ones to watch (`library-tests.yml:7-23`, `studio-unit-tests.yml:50-60`).
* You are adding a **dependency**, and need to know that you must go through the pnpm `catalog:`
  (41 entries), not a raw version, and that the version must be ≥ 3 days old.
* You are adding a **workspace package** and need the layout rules: 4 globs, `workspace:` protocol,
  `main`/`types` pointing at TypeScript source, no build script, `transpilePackages` in every Next app
  that consumes it, and `tsconfig` in the package's devDependencies.
* You are chasing a **CI failure** and need to know whether it is a hard gate or a comment.
* You are touching **generated code** and need to know which generator to run and whether the output is
  committed (all of it is) and CI-enforced (`verify-production-api-types.yml`,
  `library-tests.yml`'s registry diff, `ui-patterns-tests.yml`'s exports diff).

**Do not use / do not rely on this for:**

* **Deciding what actually blocks a merge.** The repo contains 56 workflows but *required status
  checks* live in GitHub branch-protection settings, which are not in the repository. The most accurate
  statement available from the repo is: `typecheck.yml`, `prettier.yml` and `validate-pr.yml` run on
  every PR, plus path-filtered gates for the areas you touched.
* **Expecting a package-level build.** There is none. `packages/*` ship TypeScript source; if you add a
  `build` script to a package you change Turbo's graph and the `dependsOn: ["^build"]` edges in all 8
  apps suddenly become live — check `apps/*/turbo.jsonc` `outputs` before you do.
* **Assuming lint warnings fail.** They do not. Only the ratchet gates lint, and only for the 15
  (studio) / 3 (other apps) ratcheted rules.
* **Assuming the typos gate fails.** It does not (see gotcha 1).
* **Assuming a remote Turborepo cache exists.** None is configured in-repo.
* **Running `pnpm install` right after a dependency is published**, or with a `catalog:` entry you just
  bumped, without checking the 72-hour release-age gate.
* **Assuming a Prettier/format check covers the whole repo.** It does not (`e2e/`, `scripts/`, `supabase/`,
  `docker/`, `*.astro` are outside the glob).
* **Editing generated files.** `packages/api-types/types/**`, `**/routeTree.gen.ts`, `**/__generated__/**`,
  `apps/docs/features/docs/generated/**`, `apps/www/.generated/**`,
  `supabase/functions/common/database-types.ts` — all committed, all regenerated by a script, and the
  api-types ones are diffed against production on every PR that touches them (`AGENTS.md:47`).

---

## Open questions

1. **Which checks are actually *required* to merge?** Branch-protection rules are not in the repo. The
   56 workflows and their triggers are measured; "required" is not determinable from source. Same for
   whether `studio-knip.yml` is required.
2. **Is a Turborepo remote cache active in CI?** No `TURBO_TOKEN`/`TURBO_TEAM`/`remoteCache` key exists
   in any workflow or `turbo.jsonc` (measured by grep across all 56 workflows and 9 turbo configs).
   Vercel may inject credentials into the CI environment, which is not visible here. Not measured.
3. **Do the 11 `set this to true or false` `allowBuilds` entries cause a real failure today?** I proved
   the *mechanism* (non-boolean → `ERR_PNPM_IGNORED_BUILDS`, exit 1) with pnpm 11.13.1 in a scratch
   project, and that workspace `file:` projects are exempt. I did **not** run a full install of this
   18k-file repo, so the current end-to-end install result is not measured.
4. **Actual install wall-clock time and `node_modules` size for this monorepo** — not measured (3,472
   resolved packages is the measurable proxy).
5. **How many `lint`/`typecheck` violations exist right now vs. the baselines** — the baseline totals
   are measured (1,895 / 851 / 72 / 60 / 49 / 20) but the live counts are not.
6. **Whether the `shadcn/*` warning rules are also enforced outside the ratchet** (e.g. by CodeRabbit
   path instructions) — the CodeRabbit config mentions Tailwind/motion rules in prose but does not
   enable the shadcn lint plugin. Not measured.
7. **Whether `apps/kb` (Astro) and `apps/lite-studio` (React Router) are linted at all** — measured:
   neither defines a `lint` script, and neither has an `eslint.config.cjs`. So `turbo run lint`
   (7 workspaces) skips them. Whether that is intentional is not stated in the repo.
8. **`packages/dev-tools`** has a `test` script and vitest config but I did not find a CI workflow that
   runs it — I did not exhaustively verify; there may be a path filter I missed. Not measured.
9. **The `docs-search` and `ai-commands` test suites** — `library-tests.yml` does not include
   `packages/docs-search` or `packages/ai-commands` in its path filter (`library-tests.yml:7-23`), and
   `docs-tests.yml` does include `packages/docs-search/**` (`docs-tests.yml:13`). Not fully traced.
10. **Exact `turbo` version behaviour for the `prebuild`/`postbuild` lifecycle hooks** — inferred from
    `apps/www/turbo.jsonc:12-13` and confirmed by `apps/www/turbo-build.test.ts:198-206`, but the
    turbo 2.9.14 source was not read to confirm the hook order in general.
