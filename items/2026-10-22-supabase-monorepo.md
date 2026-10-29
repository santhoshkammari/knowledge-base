---
title: Supabase monorepo: dashboard, shared packages, and build system
date: 2026-10-22
type: repo
area: infra
status: reviewed
source: https://github.com/santhoshkammari/supabase
tags: [supabase, monorepo, postgres, studio, typescript, turborepo]
last_verified: 2026-10-22
---

## Summary

**[checked]** Supabase is not one application. It is a pnpm workspace with eight apps, sixteen shared packages, one Vue block, and four end-to-end test projects. Studio is the largest product app. It contains both a Next.js pages-router runtime and a TanStack Start/Vite runtime during a migration. Shared packages are consumed as workspace source, not built and published as independent libraries. The useful lesson: trace each feature through its route, data hook, API client, and backend before changing it. This study covers the build system, Studio, and shared packages. It does not cover the self-host Docker stack or all content apps.

## What it is

**[checked]** The source is `santhoshkammari/supabase`, a public fork of `supabase/supabase`. The study read branch `master` at tree SHA `8ba2f0a63bc6d9cc00886557ffa027c5e8a83cfc`.

**[checked]** The root uses pnpm 11.13.1, Node 22 (engine minimum 22.13), and Turborepo 2.9.14. Four workspace globs are `apps/*`, `packages/*`, `blocks/*`, and `e2e/*`. The lockfile has 29 importers: the root plus 28 workspace projects. Sources: `pnpm-workspace.yaml:1-5`, root `package.json:74,84-88`, and `pnpm-lock.yaml`.

The 28 projects are eight apps, sixteen packages, one block, and four E2E projects. `examples/`, `docker/`, and `supabase/` are content trees, not pnpm workspaces. **[checked]** GitHub tree and lockfile counts; detailed counts are in [build-system notes](../research/supabase/build-system.md).

## How it works

### Build and CI

1. **[checked]** pnpm discovers workspace projects through the four globs in `pnpm-workspace.yaml:1-5`.
2. **[checked]** Internal dependencies use the `workspace:` protocol. The study measured 98 internal dependency edges across workspace manifests. See [build-system notes](../research/supabase/build-system.md).
3. **[checked]** Turborepo runs root tasks. The root config defines six tasks, and nine Turbo config files exist across the root and apps. The lockfile is 1,373,478 bytes. Sources: `turbo.jsonc:1-30`, the repository tree, and `pnpm-lock.yaml`.
4. **[checked]** CI has 56 workflow files, including 28 with pull-request triggers. Workflow names and gates are listed in [build-system notes](../research/supabase/build-system.md).

**[checked]** No package under `packages/` has a `build` script in the studied tree. Apps import shared TypeScript and CSS through workspace links. This keeps edits local, but each app's build configuration must support the source packages. Sources: package manifests and Turbo config; see [shared-package notes](../research/supabase/packages.md).

### Studio request path

**[checked]** Studio is a hybrid migration, not a plain Next.js app. Its code contains Next.js pages and TanStack routes. `STUDIO_FRAMEWORK` selects the runtime in `apps/studio/scripts/dispatch.js:34-37`; `apps/studio/AGENTS.md:25` documents both frameworks. The study measured 5,605 Studio files, 299 files under `pages/`, and 325 under `routes/`. See [Studio notes](../research/supabase/studio.md).

A typical data flow:

```text
page or route
  -> domain query or mutation in apps/studio/data/<domain>/
  -> query key and fetcher
  -> typed API client or SQL helper
  -> platform API, pg-meta, or analytics backend
```

**[checked]** The table editor uses route code, table-editor query code, and SQL mutation helpers. The SQL editor uses the content API for saved snippets and pg-meta for query execution. Logs use an infinite query and analytics SQL with cursor pagination. Paths and call chains are recorded in [Studio notes](../research/supabase/studio.md).

**[checked]** Studio uses TanStack Query v5 for server state, Valtio for shared client state, and `nuqs` for URL state. The study counted 293 `useQuery`, 326 `useMutation`, 48 Valtio importers, and 172 `nuqs` importers. Sources: `apps/studio/` tree and source grep; see [Studio notes](../research/supabase/studio.md).

### Shared packages

**[checked]** Sixteen packages hold shared UI, API types, auth, telemetry, feature flags, SQL builders, configuration, and static data. `tsconfig` has 18 workspace consumers, `config` has 14, `ui` has 11, and `common` has 9. See [package notes](../research/supabase/packages.md).

- **[checked]** `packages/ui` is the shared component library. Apps import it as source. Tailwind v4 needs apps to include shared source paths with `@source`; the study found one app without those paths. Missing paths can leave shared components unstyled. Sources: `packages/ui/` and app CSS files; package notes.
- **[checked]** `packages/pg-meta` builds SQL fragments. `SafeSqlFragment` is a branded string accepted by Studio SQL helpers. Unsafe strings need an explicit conversion path. Sources: `packages/pg-meta/src/`; package notes.
- **[checked]** `packages/api-types` commits generated Management API types. Scripts generate types from API specifications, and a production-sync workflow checks changes to the package. Sources: `packages/api-types/` and `.github/workflows/`; build-system and package notes.
- **[checked]** `packages/common` shares auth, feature-flag, telemetry, and theme code. Some apps must deep-import modules because the package barrel reaches Next.js code. Sources: `packages/common/` and consumer imports; package notes.

## Key numbers

| Measure | Value | Evidence |
|---|---:|---|
| Workspace globs | 4 | `pnpm-workspace.yaml:1-5` |
| Workspace projects, including root | 29 | `pnpm-lock.yaml` importer count |
| Apps / packages / block / E2E projects | 8 / 16 / 1 / 4 | repository tree |
| CI workflow files | 56 | `.github/workflows/` tree count |
| Studio files | 5,605 | repository tree count |
| Studio test files | 810 | `*.test.ts*` count in Studio tree |
| Internal dependency edges | 98 | workspace manifest count |
| Lockfile size | 1,373,478 bytes | `pnpm-lock.yaml` |

## Failure modes and gotchas

1. **A shared UI component renders without styles.** The app imports `packages/ui` but omits its source path from Tailwind v4 `@source`. Tailwind then does not scan those classes. Check the app stylesheet and its `@source` entries. **[checked]** `packages/ui/` and app styles; see package notes.
2. **A Studio feature exists in only one runtime.** During migration, editing only `pages/` or only `routes/` can make the feature disappear when the other runtime is selected. Check `STUDIO_FRAMEWORK` and both route trees. **[checked]** `apps/studio/AGENTS.md:25` and `apps/studio/scripts/dispatch.js:34-37`; see Studio notes.
3. **SQL query code rejects a plain string.** Studio uses branded `SafeSqlFragment` values for query helpers. Build SQL through approved builders; do not cast away the type without proving the input is safe. **[checked]** `packages/pg-meta/src/`; see package notes.
4. **A shared package import fails in a non-Next app.** The `packages/common` barrel includes Next-specific imports. Use a supported deep import when a Vite or Astro app cannot resolve that dependency. **[checked]** `packages/common/` and consumer imports; see package notes.

## When to use it

- Use this repo for the Supabase Dashboard implementation, shared UI, or API type generation.
- Use a workspace package for a shared component or contract used by several apps.
- Trace Studio features from route to data hook to fetcher to backend before changing behavior.

## When not to use it

- Do not treat this fork as canonical upstream. Compare it with `supabase/supabase` before relying on fork-specific changes.
- Do not assume all Studio code runs under one framework. Check the selected runtime.
- Do not use this study as a guide to self-host deployment. Docker, local migrations, edge functions, and most content apps remain unreviewed.

## Open questions

- Which Studio runtime runs in every production deployment path? The repo documents both runtimes, and the supporting study found conflicting production notes.
- What services and port mappings does the current self-host Docker stack use? Not checked here.
- Which CI checks are required by branch protection? Workflow files were inspected, but branch-protection settings were not.
- Are these version values still current? They describe tree SHA `8ba2f0a63bc6d9cc00886557ffa027c5e8a83cfc`, not later commits.

## Related items

- [Build system and CI deep notes](../research/supabase/build-system.md)
- [Studio deep notes](../research/supabase/studio.md)
- [Shared packages deep notes](../research/supabase/packages.md)

## Sources

- [santhoshkammari/supabase, branch `master`](https://github.com/santhoshkammari/supabase), tree SHA `8ba2f0a63bc6d9cc00886557ffa027c5e8a83cfc` (read 2026-10-22).
- Supporting source-reading reports in [`research/supabase/`](../research/supabase/), created from repository files and tree counts (2026-10-22).

### Changes

- 2026-10-22 — initial study and item.
