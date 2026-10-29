# `apps/studio` — Supabase Studio / Dashboard

Repo: `santhoshkammari/supabase` (fork of `supabase/supabase`), branch `master`.
Measured from the git tree at commit `8ba2f0a63bc6d9cc00886557ffa027c5e8a83cfc` (`/tmp/opencode/tree.json`, 21,813 entries).

**Method.** The whole `apps/studio/` tree was extracted from the repo tarball and cross-checked against the GitHub tree API: both contain **5,605 files** under `apps/studio/`, and the file lists are identical (only sort collation differs). Every number below is a `find`/`wc` count against that tree. Every claim cites `path:line` in the repo.

> The task brief said "~6640 files". Measured: **5,605**. Use 5,605.

---

## Key numbers

| Thing | Value | Where measured |
|---|---|---|
| Files under `apps/studio/` | **5,605** | `find apps/studio -type f \| wc -l` (matches tree.json) |
| Directories under `apps/studio/` | **1,035** | `find apps/studio -type d \| wc -l` |
| `.ts` files | **2,417** | extension histogram |
| `.tsx` files | **2,700** | extension histogram |
| TS/TSX lines of code | **55,315** | `wc -l` over all `.ts`/`.tsx` |
| Static assets (svg/png/jpg/webp/woff2/ttf/ico) | **427** | extension histogram |
| Test files (`*.test.ts(x)`) | **810** | `find -name "*.test.ts*" \| wc -l` |
| Test files in `tests/` (integration/component harness) | **103** | `find tests -type f \| wc -l` |
| `pages/` (Next.js pages router) files | **299** | `find pages -type f` |
| `routes/` (TanStack Router) files | **325** (221 `.tsx`) | `find routes -type f` |
| `data/` resource folders | **99** | `find data -maxdepth 1 -type d` |
| `data/**/keys.ts` query-key factories | **86** | `find data -name keys.ts` |
| `components/interfaces/` feature folders | **55** | `find components/interfaces -maxdepth 1 -type d` |
| React Query `useQuery` call sites | **293** | `grep -rhoE "useQuery[<(]"` |
| React Query `useMutation` call sites | **326** | `grep -rhoE "useMutation[<(]"` |
| `useInfiniteQuery` call sites | **25** | `grep -rhoE "useInfiniteQuery[<(]"` |
| SWR / Redux / Zustand / Jotai call sites | **0 / 0 / 0 / 0** | `grep -rhoE "from '(swr|redux|...)'"` |
| `react-hook-form` importers | **278 files** | `grep -rl react-hook-form` |
| `@hookform/resolvers` / `zodResolver` importers | **147 files** | `grep -rl zodResolver` |
| `nuqs` (URL state) importers | **172 files** | `grep -rl nuqs` |
| `valtio` (global state) importers | **48 files** | `grep -rl valtio` |
| `ui-patterns/*` imports | **1,635** | `grep -rhoE "from 'ui-patterns/"` |
| `ui` imports | **1,481** | `grep -rhoE "from 'ui'"` |
| `@supabase/pg-meta` imports | **92** | `grep -rhoE "from '@supabase/pg-meta/"` |
| `useFlag()` call sites (ConfigCat) | **152** | `grep -rn "useFlag("` |
| `useIsFeatureEnabled()` call sites | **149** | `grep -rn "useIsFeatureEnabled("` |
| Workspace packages imported by studio | 9 | `packages/*` in `package.json` (see below) |

### Versions (all from `pnpm-workspace.yaml` catalog unless noted)

| Package | Version | Cite |
|---|---|---|
| `next` | `^16.3.6` | `pnpm-workspace.yaml:45` |
| `react` / `react-dom` | `^19.2.6` | `pnpm-workspace.yaml:49-50` |
| `tailwindcss` | `^4.2.4` (v4, CSS-first `@theme`) | `pnpm-workspace.yaml:54` |
| `vite` | `^8.0.16` | `pnpm-workspace.yaml:58` |
| `vitest` | `^5.0.0` | `pnpm-workspace.yaml:60` |
| `typescript` | `~6.0.2` (`@typescript/native` = TS 7) | `pnpm-workspace.yaml:33,56` |
| `valtio` | `^2.3.2` | `pnpm-workspace.yaml:57` |
| `zod` | `3.25.76` | `pnpm-workspace.yaml:61` |
| `@tanstack/react-router` | `^1.170.44` | `pnpm-workspace.yaml:22` |
| `@tanstack/react-start` | `^1.169.2` | `pnpm-workspace.yaml:23` |
| `@tanstack/react-query` | `~5.104.3` | `apps/studio/package.json:86` |
| `react-hook-form` | `^7.71.2` | `apps/studio/package.json:149` |
| `nuqs` | `2.7.1` | `apps/studio/package.json:136` |
| `@supabase/auth-js` | `2.117.3` (catalog) | `pnpm-workspace.yaml:17` |
| `@supabase/supabase-js` | `2.117.3` (catalog) | `pnpm-workspace.yaml:21` |
| `msw` | `^2.3.0` | `apps/studio/package.json:219` |
| `@configcat/sdk` | `^1.1.0` | `apps/studio/package.json:45` |

Workspace deps (`apps/studio/package.json`): `ai-commands`, `api-types`, `common`, `config`, `dev-tools`, `icons`, `@supabase/pg-meta`, `shared-data`, `ui`, `ui-patterns` — lines 79, 100, 101, 102, 106, 159, 160.

---

## 1. App stack

**It is a hybrid, mid-migration app: Next.js *pages* router and TanStack Start run side-by-side.**

> "Next.js pages router + TanStack Start (mid-migration, see below), React 19. Dev server: `pnpm dev:studio` → http://localhost:8082."
> — `apps/studio/AGENTS.md:3`

> "Both runtimes ship side-by-side; the `STUDIO_FRAMEWORK` env var selects which one `pnpm dev`/`build` runs (default: `next`, resolved in `scripts/dispatch.js`)."
> — `apps/studio/AGENTS.md:25`

| Concern | Answer | Evidence |
|---|---|---|
| Framework | Next.js 16 **pages router** (not app router) + TanStack Start 1.x on Vite 8 | `AGENTS.md:3,25`; `apps/studio/next.config.ts:55-230`; `apps/studio/vite.config.ts:836-844` (`tanstackStart({srcDirectory:'./', spa:{enabled:true}})`) |
| App Router | Only 4 files in `apps/studio/app/` — two route handlers (`app/api/status-page/route.ts`, `app/api/scoped-access-token-permissions/route.ts`) plus a helper and its test. Not a real App Router app. | `find apps/studio/app -type f` |
| React | 19.2 (`^19.2.6`) | `pnpm-workspace.yaml:49` |
| Tailwind | v4, CSS-first. `@theme` blocks in `styles/globals.css`, `@source` globs for Tailwind 4 content scanning; PostCSS only for the Next build. | `apps/studio/styles/globals.css:1-8,10-30`; `apps/studio/vite.config.ts:743-750`; `apps/studio/package.json:182-183` |
| Global state | **valtio** proxies (`state/`), 48 importers | `pnpm-workspace.yaml:57`; `apps/studio/state/tabs.tsx:12` (`import { proxy, subscribe, useSnapshot } from 'valtio'`) |
| URL state | **nuqs** (172 importers) | `apps/studio/package.json:136`; `apps/studio/pages/_app.tsx:34` (`NuqsAdapter` from `nuqs/adapters/next/pages`) |
| Data fetching | **TanStack React Query v5** — 293 `useQuery` + 326 `useMutation` + 25 `useInfiniteQuery` call sites; 0 SWR | `apps/studio/package.json:86`; measured grep counts above |
| Forms | **react-hook-form** + **zod** via `@hookform/resolvers`; 278 / 147 importers | `apps/studio/package.json:149,55,172`; `apps/studio/AGENTS.md:37` ("react-hook-form + zod for forms") |
| Validation | zod (`zod: 3.25.76`) — also used to parse OpenAPI responses at the wire boundary | `pnpm-workspace.yaml:61`; `apps/studio/data/tables/tables-query.ts:21-22` |
| Dates | **dayjs** (not date-fns), plugins preloaded at both entries | `apps/studio/AGENTS.md:86`; `apps/studio/pages/_app.tsx:85-90` |
| Icons | `lucide-react`, always with the `Icon` suffix (lint-enforced) | `apps/studio/AGENTS.md:87` |
| Tables | `@tanstack/react-table` (new code). `react-data-grid` is banned for new code; still used for the logs grid. | `apps/studio/AGENTS.md:88`; `apps/studio/package.json:144` |
| HTTP client | `openapi-fetch` typed by generated `api-types` — **all platform calls go through `data/fetchers.ts`, never raw `fetch`** | `apps/studio/AGENTS.md:36`; `apps/studio/data/fetchers.ts:31-44` |
| i18n | **None.** No `next-intl`/`react-intl`/`lingui`/`i18n` config anywhere; `compat/next/router.ts:349-351` explicitly says "i18n routing isn't wired through TanStack here". All copy is English literals. | grep over `apps/studio` for `i18n\|useTranslation\|next-intl\|react-intl` → only the compat shim comment |
| Error reporting | Sentry — `@sentry/nextjs` for Next, `@sentry/tanstackstart-react` for Vite | `apps/studio/next.config.ts:4,238-267`; `apps/studio/vite.config.ts:7,853-873` |
| Monorepo tooling | pnpm workspaces + turbo | `pnpm-workspace.yaml:1-5`; `apps/studio/turbo.jsonc` |

**Workspace package split** (studio consumes these as source, not as built artifacts — `transpilePackages`):

> `transpilePackages: ['ui', 'ui-patterns', 'common', 'shared-data', 'api-types', 'icons']`
> — `apps/studio/next.config.ts:202`

| Package | Files | Role |
|---|---|---|
| `packages/ui-patterns` | 269 | Composed patterns (`ConfirmationModal`, `Admonition`, `EmptyState`, …) — 1,635 imports |
| `packages/ui` | 194 | shadcn-style primitives — 1,481 imports |
| `packages/pg-meta` | 147 | SQL builders + Zod schemas (`pgMeta.tables.list().sql`, `getTablesPaginatedSql`) — 92 imports |
| `packages/common` | 99 | Auth, telemetry, feature flags, theme, `useParams` |
| `packages/icons` | 87 | Generated icon set |
| `packages/shared-data` | 15 | Scoped-PAT permission catalog, regions, pricing |
| `packages/api-types` | 15 | **Generated** OpenAPI types: `types/api-v1.d.ts`, `api-v2.d.ts`, `platform.d.ts` (`packages/api-types/index.ts:1-20`; codegen script `packages/api-types/package.json:11`) |

---

## 2. How a data-backed page is wired end to end

**The universal shape** (documented in `apps/studio/AGENTS.md:36` and `.agents/skills/studio-queries/SKILL.md`):

```
route file (pages/**  +  mirror routes/**)
  → hook in data/<domain>/<x>-query.ts        (useQuery / useInfiniteQuery / useMutation)
    → key factory in data/<domain>/keys.ts   (array key, `as const`)
    → fetch in data/fetchers.ts              (openapi-fetch `get`/`post`/`put`/`del`)
      → handleError(error)                   (throws a typed ResponseError subclass)
    ← typed data (api-types / zod)
```

There are **three different backends** reachable from the same client:

1. **Platform API / Management API** — `https://api.supabase.com` via `NEXT_PUBLIC_API_URL`. Paths like `/platform/...` and `/v1/projects/{ref}/...`.
2. **pg-meta** — a Go sidecar that runs SQL against the *user's* database. Path `/platform/pg-meta/{ref}/query`. On platform the connection string is encrypted and sent in the `x-connection-encrypted` header.
3. **Analytics (ClickHouse/Logflare)** — path `/platform/projects/{ref}/analytics/endpoints/logs.all[.otel]`.

### Example A — Table Editor (route → hook → pg-meta → Postgres)

**Route.** `apps/studio/pages/project/[ref]/editor/[id].tsx:16-27` reads `id` + `ref` from `useParams()` (from `common`, camelCased) and calls `useTableEditorQuery`. The TanStack mirror is `apps/studio/routes/project/$ref/editor/$id.tsx:3-11`, which imports the **same** page component and renders it with `dehydratedState={undefined}` — the "Path A re-export" migration pattern (`apps/studio/TANSTACK_MIGRATION.md:36-40`).

**Hook.** `apps/studio/data/table-editor/table-editor-query.ts:19-34`:
```ts
const sql = getTableEditorSql({ id })          // SQL from @supabase/pg-meta
const { result } = await executeSql({ projectRef, connectionString, sql, queryKey: ['table-editor', id] }, signal)
```
Hook itself at `:41-60` — `useQuery` with `queryKey: tableEditorKeys.tableEditor(projectRef, id)`, `enabled` gated on `projectRef` and `id` being defined, `staleTime: 5 * 60 * 1000`.

**API client.** `apps/studio/data/sql/execute-sql-mutation.ts:76-220` — the single SQL execution path:
- `:96-100` rejects SQL larger than 0.98 MB ("Query is too large to be run via the SQL Editor").
- `:103` sets `x-connection-encrypted: connectionString`.
- `:130-159` optional `preflightCheck`: runs `explain <sql>` first and aborts if cost ≥ `COST_THRESHOLD = 200_000` (`:32-33`).
- `:163-171` `POST QUERY_SOURCE_REGISTRY.database.endpoint` = `/platform/pg-meta/{ref}/query` (`apps/studio/data/query-sources/query-source-registry.ts:60-71`).
- `:177-209` maps the error; `:211-219` unwraps the role-impersonation sentinel.

**Transport.** `apps/studio/data/fetchers.ts:31-44` creates the `openapi-fetch` client; `:130-175` installs two middleware — one that injects auth + `X-Request-Id` (`:53-65`) and one that normalises errors (adds `code`, `requestId`, `retryAfter`, `requestPathname`).

**Backend.** pg-meta connects to the user's Postgres. `apps/studio/data/fetchers.ts:108-127` (`pgMetaGuard`) short-circuits with a 400 "API Error: happened while trying to acquire connection to the database" when the encrypted connection string is missing on platform.

**Downstream.** `apps/studio/components/interfaces/TableGridEditor/TableGridEditor` renders the grid; row writes go through `data/table-rows/table-row-update-mutation.ts` and `table-row-truncate-mutation.ts`.

### Example B — SQL Editor (two backends behind one snippet)

**Route.** `apps/studio/pages/project/[ref]/sql/[id].tsx:28-66`. The snippet *content* comes from the **content API** (`useSqlSnippetByIdQuery` → `apps/studio/data/content/content-id-query.ts`), not from Postgres. The *execution* goes to pg-meta.

**Execution.** `apps/studio/components/interfaces/SQLEditor/useSqlEditorExecution.ts` → `useExecuteSqlMutation` (`apps/studio/data/sql/execute-sql-mutation.ts:224-283`), which:
- parses the SQL to emit table-level telemetry events (`:241-254`),
- on success, invalidates every `['projects', projectRef, ...]` React Query key **except** a hard-coded ignore list `['branches','settings-v2','addons','custom-domains','content']` (`:24`, `:263-272`).

**Snippet source is a first-class field.** A snippet can target the *logs* backend instead of the database: `apps/studio/state/tabs.tsx:67-77` documents `metadata.sqlSource: 'database' | 'logs'`, and `apps/studio/data/query-sources/query-source-registry.ts:60-71` is the closed registry of the two backends.

### Example C — Logs Explorer (analytics backend)

**Route.** `apps/studio/pages/project/[ref]/logs/index.tsx` + 15 sibling log pages (`postgres-logs.tsx`, `auth-logs.tsx`, `pgcron-logs.tsx`, …).

**Hook.** `apps/studio/data/logs/unified-logs-infinite-query.ts:156-192` — `useInfiniteQuery` with a **cursor** pagination scheme (`getNextPageParam` returns `{cursor, direction, row}`), `staleTime` 5 min, `refetchOnWindowFocus: false` (`:27-33`).

**Backend selection is a flag.** `:39-42` — `useUnifiedLogsBackend()` reads the ConfigCat flag `otelUnifiedLogs` (default `true`), which picks between two SQL builders (`UnifiedLogs.queries.ts` vs `UnifiedLogs.queries.bq`) and two endpoints.

**Endpoint.** `apps/studio/data/logs/logs-endpoint.ts:1-4`:
```ts
useOtel ? '/platform/projects/{ref}/analytics/endpoints/logs.all.otel'
        : '/platform/projects/{ref}/analytics/endpoints/logs.all'
```

**Query builder is SQL, sent as a string.** `:100-122` builds a `safeSql`-branded fragment with a `TIMESTAMP_MICROS`/`parseDateTime64BestEffort` timestamp cast depending on backend, then `LIMIT 50`.

**Wire boundary.** `apps/studio/data/logs/execute-analytics-sql.ts:41-76` — the only place analytics SQL may leave the browser. It accepts **only** `SafeLogSqlFragment`; plain strings are a compile error (`:11`, `:25-27`). The file header cites `.agents/skills/safe-sql-execution/SKILL.md`.

### Example D — Storage buckets (platform API, paginated)

`apps/studio/data/storage/buckets-query.ts:41-52` — `GET /platform/storage/{ref}/buckets` with `limit`/`offset`/`sortColumn`/`sortOrder`/`search` query params, then `useInfiniteQuery` at `:167-197` (page-number pagination, `keepPreviousData`), plus a bespoke retry policy at `:206-224` that **stops retrying** on 404 or "Missing tenant config"/"Project has no active API keys".

### Example E — API keys (platform API, `IS_PLATFORM`-gated)

`apps/studio/data/api-keys/legacy-api-keys-status-query.ts:17-26` — `GET /v1/projects/{ref}/api-keys/legacy`; the hook's `enabled` includes `IS_PLATFORM` (`:38`).

### Wire-level details worth knowing

- **Auth header**: `apps/studio/data/fetchers.ts:53-65` sets `Authorization: Bearer <accessToken>` unless already present, plus `X-Request-Id: <uuid4>`.
- **Empty-body responses**: `apps/studio/data/fetchers.ts:67-106` — `openapi-fetch` only treats 204 / `Content-Length: 0` as empty; HTTP/3 can omit the header, which produced "Unexpected end of JSON input" on a successful `201`. `normalizeEmptyBodyResponse` patches the header.
- **Query retry policy**: `apps/studio/data/query-client.ts:14-23` skips retries on 4xx (except 429) and on a hard-coded path list; `:26-35` detects `canceling statement due to statement timeout` specifically on `/platform/pg-meta/:ref/query`.
- **Global stale time**: 60 s (`apps/studio/data/query-client.ts:41`); `MAX_RETRY_FAILURE_COUNT = 3` (`:21`).

---

## 3. Auth and session handling

### The client

`apps/studio/packages/common/gotrue.ts:183-194` builds a raw `@supabase/auth-js` `AuthClient` (not `supabase-js`):

```ts
export const gotrueClient = new AuthClient({
  url: process.env.NEXT_PUBLIC_GOTRUE_URL,
  storageKey: STORAGE_KEY,                                   // 'supabase.dashboard.auth.token'
  detectSessionInUrl: shouldDetectSessionInUrl,
  debug: debug ? (persistedDebug ? logIndexedDB : true) : false,
  lock: navigatorLockEnabled ? debuggableNavigatorLock : undefined,
  experimental: { recoveryCodes: true },
  ...('localStorage' in globalThis ? { storage: globalThis.localStorage, userStorage: globalThis.localStorage } : null),
})
```

- **Credential storage**: browser `localStorage` under `supabase.dashboard.auth.token` (`packages/common/gotrue.ts:5`, `:191-193`). Overridable with `NEXT_PUBLIC_STORAGE_KEY`.
- **Cross-tab locking**: `navigator.locks` via auth-js `navigatorLock` (`packages/common/gotrue.ts:33-45`, `:160`). A debug wrapper broadcasts "who-is-holding-the-lock" on a BroadcastChannel and reports lock contention to Sentry after 10 s (`:129-181`).
- **Optional IndexedDB audit log** of auth events, enabled by `NEXT_PUBLIC_AUTH_PERSISTED_KEY=true` (`packages/common/gotrue.ts:49-118`). It strips `user`, `access_token`, `token_type`, `provider_token` before writing (`:82-89`).
- **Debug mode** via `NEXT_PUBLIC_AUTH_DEBUG_KEY` (`packages/common/gotrue.ts:26-27`).

### The React layer

`packages/common/auth.tsx:69-123` — `AuthProvider` holds `{session, error, isLoading}`:
- `:75-86` `gotrueClient.initialize()` on mount.
- `:88-102` `onAuthStateChange` subscription keeps state in sync; a session clears the error.
- `:104-112` `refreshSession()` calls `gotrueClient.refreshSession()`.
- `:114-120` `alwaysLoggedIn` short-circuits to a `DEFAULT_SESSION` stub (`:19-40`).

Hooks: `useAuth` (`:127`), `useSession` (`:129`), `useUser` (`:131-140`), `useIsLoggedIn` (`:144-148`), `useIsMFAEnabled` (`:152-156`).

`packages/common/auth.tsx:172-185` — **`getAccessToken()`**, the function every data request uses:
```ts
if (typeof window === 'undefined') return undefined
const { data: { session }, error } = await gotrueClient.getSession()
if (error) throw error
return session?.access_token
```
`getSession()` refreshes the token if it is near expiry — that is the refresh path.

### Attaching credentials to requests

`apps/studio/data/fetchers.ts:59-62`:
```ts
if (!headers.has('Authorization')) {
  const accessToken = await getAccessToken()
  if (accessToken) headers.set('Authorization', `Bearer ${accessToken}`)
}
```
The client is also created with `credentials: 'include'` (`apps/studio/data/fetchers.ts:37`) so platform cookies ride along.

### Sign-out

- `packages/common/auth.tsx:158` — `signOut()` → `gotrueClient.signOut()`.
- `packages/common/auth.tsx:160-163` — `logOut()` = `signOut()` **plus `clearLocalStorage()`** (from `packages/common/constants/local-storage.ts`).
- `apps/studio/lib/auth.tsx` exposes `useSignOut()`; `apps/studio/hooks/misc/withAuth.tsx:35,98-100` calls it before redirecting to `/sign-in`.
- `apps/studio/pages/logout.tsx` exists as a dedicated route.

### Page-level gate: `withAuth`

`apps/studio/hooks/misc/withAuth.tsx:15-167`:
- `:29-31` — **on self-hosted (`!IS_PLATFORM`) the HOC is a no-op** and returns the component untouched (`AGENTS.md:38`).
- `:41-49` — checks the **authenticator assurance level (AAL)** via `useAuthenticatorAssuranceLevelQuery()`; `isAtHighestAAL = aalData.currentLevel === aalData.nextLevel`. `useHighestAAL` defaults to `true` (`:17-26`).
- `:51-57` / `:61-67` — toasts on AAL / permissions fetch failure.
- `:13`, `:103-120` — if auth hasn't resolved within **10 s**, a `SessionTimeoutModal` opens.
- `:75-101` — redirect logic: AAL1-but-needs-AAL2 → `/sign-in-mfa?returnTo=…` (session preserved, for IdP-initiated SSO); otherwise sign out then `/sign-in?returnTo=…`.

### Platform vs self-hosted

`apps/studio/lib/constants/index.ts:5` — `IS_PLATFORM = process.env.NEXT_PUBLIC_IS_PLATFORM === 'true'`.
`apps/studio/lib/constants/index.ts:12` — `IS_CLI = !IS_PLATFORM && !!process.env.CURRENT_CLI_VERSION` (CLI-launched Studio).
`apps/studio/lib/constants/index.ts:35-46` — `API_URL` resolution: `http://localhost:3000/api` in test mode, `NEXT_PUBLIC_API_URL` on platform, `/api` in the browser when self-hosted.

---

## 4. Feature flags and telemetry

**Two separate flag systems.** `apps/studio/AGENTS.md:85`: *"`useIsFeatureEnabled` for product features, `useFlag` from `'common'` for feature flags — two different systems."*

### A. Product features — static JSON + per-user disable list

`packages/common/enabled-features/index.ts`:
- `:1` loads `enabled-features.json` from the package.
- `:26-28` any feature whose JSON value is falsy is *disabled by default*.
- `:50-83` `isFeatureEnabled(features, runtimeDisabledFeatures)`.
- `:61-66` `ENABLED_FEATURES_OVERRIDE_DISABLE_ALL=true` disables everything (used to build a filtered docs search index).
- `:7-24` runtime features that the platform can disable per user (`organizations:create`, `billing:invoices`, `realtime:all`, …).

`apps/studio/hooks/misc/useIsFeatureEnabled.ts:11-25` merges two sources:
1. `profile.disabled_features` (from `useProfile()`),
2. `override.disabled_features` (from `useEnabledFeaturesOverrideQuery()` → `apps/studio/data/misc/enabled-features-override-query.ts`).

**149 call sites** (measured).

### B. Feature flags — ConfigCat + PostHog

`packages/common/feature-flags.tsx:99-297` — `FeatureFlagProvider`:
- `:176-191` loads **both** providers in parallel with `Promise.allSettled`, so one failing does not block the other.
  - **PostHog**: `GET {API_URL}/telemetry/feature-flags?organization_slug=&project_ref=` (`:26-49`) — the platform proxies PostHog flags.
  - **ConfigCat**: `getFlags(userEmail, customAttributes)` from `packages/common/configcat.ts`.
- `:130-160` before fetching flags it posts org/project context to `/telemetry/identify` so flag targeting can use group properties.
- `:199-228` **dev-toolbar overrides**: cookie `x-ph-flag-overrides` (PostHog) and `x-cc-flag-overrides` (ConfigCat), active only when `NEXT_PUBLIC_ENVIRONMENT` is `local` or `staging`.
- `:236-251` ConfigCat overrides merge `vercel-flag-overrides` then `x-cc-flag-overrides` (local wins).
- `:293` ConfigCat values are exposed to the `flags/react` `<FlagValues>` provider.
- `:307-322` `useFlag(name)` reads the ConfigCat store; returns `false` and logs `console.error` when the key does not exist.

ConfigCat custom attributes are set in `apps/studio/pages/_app.tsx:110-133`: `cloud_provider`, `plan`, `organization_slug`, `organization_created_at`.

**152 `useFlag()` call sites** (measured). Example: `otelUnifiedLogs` picks the logs backend (`apps/studio/data/logs/unified-logs-infinite-query.ts:40`).

### C. Telemetry — PostHog + a first-party event endpoint

`apps/studio/lib/telemetry/track.ts` — the typed wrapper:
- `:11-22` `EventMap` is derived from `TelemetryEvent` in `packages/common/telemetry-constants.ts` — the event catalogue is a **shared package**, not app-local.
- `:33-73` `useTrack()` auto-injects `{project: projectRef}` and `{organization: orgSlug}` groups plus the current pathname.
- `:66` `track(action, properties?, groupOverrides?)`.

`packages/common/telemetry.tsx:430-462` — `sendTelemetryEvent(API_URL, event, pathname)`:
- `:431-432` **no-op unless the user consented** (`hasConsented()`).
- `:434-439` body = `{...getSharedTelemetryData(pathname), action, custom_properties, groups}`; body shape is `components['schemas']['TelemetryEventBodyV2']` from `api-types`.
- `:456-461` `POST {API_URL}/telemetry/event` with header `Version: 2`; `keepalive` only for 4 "survive navigation" actions (`:423-428`).

**What is sent**: page URL, pathname, hostname, referrer + referring domain, page title, `session_id` (written to a cookie at `:215-217`), `$groups` (organization/project), and every active feature flag flattened as `$feature/<key>` (`:233-235`). First-touch attribution (`utm_*`, `gclid`, `fbclid`, `ttclid`, `msclkid`, `oppref`, …) is parsed from the URL and from a first-referrer cookie (`:75-120`, `:167-203`).

**PostHog (client SDK)**: `packages/common/posthog-client.ts` wraps `posthog-js`:
- `:94-96` `autocapture`, `capture_pageview`, `capture_pageleave` are all **off** — Studio sends them manually.
- `:83-148` `init()` queues up to **20** pending events (`MAX_PENDING_EVENTS`, `:13`) until the SDK loads.
- `:150-200` page views / page leaves use `transport: 'sendBeacon'`.
- `:45-54` session recording is **off by default**; each app must pass its own masking policy via `buildSessionRecordingConfig`.
- `:321-346` `getFeatureFlag` reads client-side PostHog flags; in `NODE_ENV=development` the `x-ph-flag-overrides` cookie wins.
- `:381-417` experiment exposure is deduplicated per session via `sessionStorage` key `ph_exposed:<experimentId>`.
- `:56-81` host defaults: `NEXT_PUBLIC_POSTHOG_HOST` → `https://ph.supabase.green`; UI host `https://eu.posthog.com`.

**Consent**: `packages/common/consent-state.ts` + `packages/common/consent-state.test.ts`. Every telemetry function early-returns without consent.

**Other telemetry surfaces**: Google Tag Manager is only injected when `IS_PLATFORM && NEXT_PUBLIC_GOOGLE_TAG_MANAGER_ID && hasAccepted` (`packages/common/telemetry.tsx:48-73`). Sentry captures exceptions; `apps/studio/data/fetchers.ts:193-258` (`handleError`) captures with `alwaysCapture` and always rethrows a typed `ResponseError` subclass.

**Telemetry event catalogue size**: not measured (file is `packages/common/telemetry-constants.ts`; event count not counted — see Open questions).

---

## 5. Biggest directories (measured)

### Depth 1 (files directly under `apps/studio/<dir>/`)

| Files | Dir | What it is |
|---|---|---|
| **2,976** | `components/` | All UI. Split into `interfaces/` (2,305 — per-product feature folders), `ui/` (339 — app-local widgets), `layouts/` (244 — shells: Project, Auth, Storage, SQL Editor…), `grid/` (83 — the table grid / SupabaseGrid) |
| **849** | `data/` | React Query layer: 99 resource folders, 86 `keys.ts`, one folder per API domain |
| **398** | `public/` | Static assets (309 in `img/`, 60 in `favicon/`, 20 Monaco workers) |
| **325** | `routes/` | TanStack Router tree (221 `.tsx` route files) + `routeTree.gen.ts` (generated, never hand-edit — `AGENTS.md:31`) |
| **299** | `pages/` | Next.js pages router + `pages/api/` (102 API route handlers) |
| **293** | `lib/` | Cross-cutting helpers: `ai/` (106 — the Assistant), `api/` (45), `constants/` (8), `telemetry/` (5), `validation/`, `forms/`, `server/` |
| **108** | `hooks/` | `misc/` (71), `analytics/` (15), `custom-content/`, `ui/`, `ai/` |
| **103** | `tests/` | Component/page integration harness (`tests/lib/` MSW helpers, `tests/config/`, `tests/features/`) |
| **102** | `state/` | valtio stores: `shortcuts/` (50 — the keyboard-shortcut registry), `sql-editor/` (17), `notebooks/` (5), plus 31 top-level store files (`tabs.tsx`, `ai-assistant-state.tsx`, `table-editor.tsx`, …) |
| 33 | `static-data/` | `integrations/` (33) — integration overview markdown + metadata |
| 18 | `compat/` | `next/` (15) — shims so legacy pages keep working under Vite (`next/router`, `next/link`, `next/image`, `next/head`, `next/server`, `next/navigation`, `next/dynamic`, `next/script`, `next/compat/router`) |
| 15 | `evals/` | Braintrust evals for the Assistant |
| 13 | `styles/` | CSS: `globals.css` (Tailwind v4 theme), `grid.css`, `monaco.css`, `storage.css`, … |
| 11 | `scripts/` | `dispatch.js` (framework dispatcher), `vercel-spa-routes.ts`, `clean-turbopack-cache.mjs`, `deno-types.ts`, `codegen.ts` |
| 9 | `types/` | Shared TS types (`ResponseError`, `NextPageWithLayout`, …) |
| 8 | `fonts/` | `next/font` sources (Inter, Manrope, Source Code Pro) |
| 4 | `__mocks__/` | Manual mocks for `hooks/analytics/*` |
| 4 | `app/` | The only Next **App Router** files (2 route handlers) |
| 35 | *(root files)* | `next.config.ts`, `vite.config.ts`, `vitest.config.ts`, `router.tsx`, `server.ts`, `start.ts`, `vercel.ts`, `Dockerfile`, `AGENTS.md`, `TANSTACK_MIGRATION.md`, … |

### Depth 2 — `components/interfaces/` (55 feature folders, 2,305 files)

| Files | Folder | Files | Folder |
|---|---|---|---|
| 284 | `Database/` | 55 | `Explorer/` |
| 203 | `Storage/` | 51 | `UnifiedLogs/` |
| 198 | `Organization/` | 48 | `Functions/` |
| 192 | `Settings/` | 47 | `Support/` |
| 184 | `Integrations/` | 44 | `App/` |
| 110 | `Auth/` | 36 | `QueryPerformance/` |
| 98 | `Account/` | 35 | `Reports/` |
| 89 | `ConnectSheet/` | 34 | `DiskManagement/` |
| 78 | `TableGridEditor/` | 31 | `QueryInsights/` |
| 66 | `SQLEditor/` | 30 | `ProjectHome/` |

### Depth 2 — `data/` top folders

`storage/` 57 · `replication/` 39 · `organizations/` 34 · `database/` 33 · `content/` 31 · `config/` 28 · `projects/` 26 · `logs/` 22 · `privileges/` 21 · `integrations/` 21 · `auth/` 21 · `reports/` 17 · `oauth-apps/` 17 · `database-queues/` 16 · `table-rows/` 15 · `profile/` 15 · `analytics/` 15.

---

## 6. Test setup

### Runner

**Vitest 5** (`pnpm-workspace.yaml:60`) with **MSW 2** for HTTP mocking and **jsdom**.

`apps/studio/vitest.config.ts`:
- `:23` `environment: 'jsdom'` globally (with a TODO to move it per-file).
- `:25` `retry: IS_CI ? 2 : 0` — flaky retries **only in CI**.
- `:26-30` setup files: `tests/setup/polyfills.ts`, `tests/vitestSetup.ts`, `tests/setup/radix.js`.
- `:32-37` excludes `.next/*` plus **two specific test files** that are known-broken: `tests/features/logs/logs-query.test.tsx` and `tests/features/reports/storage-report.test.tsx`.
- `:39-47` coverage: reporters `text`, `text-summary`, `lcov`; `include: ['lib/**/*.ts']` — **coverage is collected for `lib/**` only**, not for `components/` or `data/`.

### Scripts

`apps/studio/package.json:21-26`:
```
test        → vitest --run --coverage
test:watch  → vitest watch
test:ui     → vitest --ui
test:update → vitest --run --update
test:ci     → vitest --run --coverage
test:report → open coverage/lcov-report/index.html
```

### Where tests live

Two conventions coexist (810 test files total):

1. **Co-located** next to the source — `*.test.ts` / `*.test.tsx`. Distribution: `components/` 484, `lib/` 106, `tests/` 88, `data/` 68, `hooks/` 27, `state/` 22, `compat/` 4, root 4, `evals/` 3, `scripts/` 2, `static-data/` 1, `app/` 1.
2. **`tests/`** (103 files) — cross-cutting suites: `tests/pages/**` (page-level integration, 27 files), `tests/components/**` (40), `tests/features/**` (14), `tests/lib/**` (MSW + `customRender` helpers), `tests/config/` (router mock), `tests/setup/`.

### Harness

`apps/studio/AGENTS.md:40`: *"component tests use `customRender` + `addAPIMock` from `tests/lib/`; unhandled network requests fail tests. Don't `vi.mock('@/data/...')`."*

Helpers: `tests/lib/custom-render.tsx`, `tests/lib/msw.ts`, `tests/lib/msw-global-api-mocks.ts`, `tests/lib/route-mock.ts`, `tests/lib/disabled-matchers.ts`, `tests/lib/sql-editor-test-utils.tsx`, `tests/lib/branch-test-utils.ts`.

### CI

| Gate | Workflow | Command |
|---|---|---|
| Unit + coverage | `.github/workflows/studio-unit-tests.yml:81` | `pnpm run test:ci` in `apps/studio`; lcov artifact uploaded (`:83-88`) and pushed to Coveralls (`:108-115`, `continue-on-error: true`) |
| Dead code | `.github/workflows/studio-knip.yml:65` | `pnpm knip --workspace apps/studio --reporter symbols --reporter github-actions` |
| Lint ratchet | `.github/workflows/studio-lint-ratchet.yml:49` | `pnpm --filter studio run lint:ratchet` |
| Typecheck + lint | `.github/workflows/typecheck.yml:59-65` | `pnpm run typecheck`, `pnpm run lint`, plus `node scripts/check-case-hazards.mjs` first (`:47-48`) |
| E2E (self-hosted) | `.github/workflows/studio-e2e-test.yml` | Playwright, matrix `framework: [next, tanstack]` × 2 shards; `supabase start --exclude studio,mailpit` → build → `pnpm e2e --shard=N/2` |
| Assistant evals | `.github/workflows/braintrust-evals.yml` | `braintrust eval` |

**Coverage expectations**: there is **no numeric coverage threshold** in the repo (no `thresholds` in `vitest.config.ts:39-47`). The gate is *lint ratchet* + *knip*, and `AGENTS.md:40` says "default to including relevant tests with any change … 'no tests' should be a considered choice, not the default."

**Lint ratchet**: `apps/studio/AGENTS.md:80` — "the per-rule occurrence count must not increase, so a new `any`, unresolved `exhaustive-deps` warning, or default export fails the build even though it's 'only a warning'."

---

## 7. Local development

### Run it

```bash
pnpm install          # pnpm only: "preinstall": "npx only-allow pnpm"
pnpm run dev          # apps/studio/package.json:9 → node scripts/dispatch.js dev
# → http://localhost:8082
```
Root: `pnpm dev:studio` = `turbo run dev --filter=studio` (`package.json:8`).
`apps/studio/AGENTS.md:3` and `apps/studio/README.md:36-56`.

### Framework switch

`apps/studio/scripts/dispatch.js:34-37` reads `STUDIO_FRAMEWORK` from the shell env, then `.env.local`, then `.env` (`:34-35`) and resolves to `dev:next` / `dev:tanstack` (default `next`, `:36`).

| Script | Command | Cite |
|---|---|---|
| `dev:next` | `next dev -p ${STUDIO_PORT:-8082}` | `package.json:12` |
| `dev:tanstack` | `NODE_OPTIONS=--max-old-space-size=8192 vite dev --port ${STUDIO_PORT:-8082}` | `package.json:15` |
| `build:next` | `next build` (+ static asset upload) | `package.json:13` |
| `build:tanstack` | `vite build --mode ${MODE:-production}` | `package.json:16` |
| `start:tanstack` | `node --env-file-if-exists=.env … .output/server/index.mjs` | `package.json:17` |

### Required env vars

`apps/studio/.env` (committed; the source of truth for self-hosted defaults):

| Var | Default in `.env` | Cite |
|---|---|---|
| `PORT` | `8082` | `.env:2` |
| `STUDIO_PG_META_URL` | `http://localhost:8000/pg` | `.env:3` |
| `POSTGRES_PASSWORD` | placeholder | `.env:4` |
| `DEFAULT_ORGANIZATION_NAME` / `DEFAULT_PROJECT_NAME` | `Default Organization` / `Default Project` | `.env:6-7` |
| `DASHBOARD_USERNAME` / `DASHBOARD_PASSWORD` | `supabase` / insecure placeholder | `.env:8-9` |
| `SUPABASE_URL` / `SUPABASE_PUBLIC_URL` | `http://localhost:8000` | `.env:11-12` |
| `SUPABASE_ANON_KEY` / `SUPABASE_SERVICE_KEY` | demo JWTs | `.env:13-14` |
| `LOGFLARE_URL` | `http://localhost:4000` | `.env:18` |
| `NEXT_PUBLIC_SITE_URL` | `http://localhost:3000` | `.env:23` |
| `NEXT_PUBLIC_GOTRUE_URL` | `$SUPABASE_PUBLIC_URL/auth/v1` | `.env:24` |
| `NEXT_PUBLIC_HCAPTCHA_SITE_KEY` | `10000000-ffff-…` (test key) | `.env:25` |
| `DOCKER_SOCKET_LOCATION` | `/var/run/docker.sock` | `.env:31` |

Platform mode adds `NEXT_PUBLIC_IS_PLATFORM=true` and `NEXT_PUBLIC_API_URL`. The **complete** list of env vars turbo must declare is `apps/studio/turbo.jsonc:7-126` (≈100 entries, including `NEXT_PUBLIC_CONFIGCAT_SDK_KEY`, `NEXT_PUBLIC_POSTHOG_KEY` via the PostHog client, `LOGFLARE_*`, `SENTRY_*`, `PLATFORM_PG_META_URL`, `PG_META_CRYPTO_KEY`, `PGRST_DB_*`, `OPENAI_API_KEY`, `BRAINTRUST_*`, `STUDIO_FRAMEWORK`, `MODE`).

### Services Studio talks to

| Service | How Studio reaches it | Cite |
|---|---|---|
| **Postgres** (user DB) | Directly, via pg-meta. Platform: encrypted connection string in the `x-connection-encrypted` header. Self-hosted: `STUDIO_PG_META_URL`. | `data/fetchers.ts:103,108-127`; `.env:3` |
| **pg-meta** (Go sidecar, `/pg`) | `STUDIO_PG_META_URL` self-hosted; `PLATFORM_PG_META_URL` platform | `.env:3`; `lib/constants/index.ts:48-50` |
| **Platform API / Management API** | `NEXT_PUBLIC_API_URL`; paths `/platform/*` and `/v1/*` | `lib/constants/index.ts:35-46`; `data/fetchers.ts:34` |
| **GoTrue / Auth** | `NEXT_PUBLIC_GOTRUE_URL` (browser); `SUPABASE_URL` server-side | `.env:24`; `packages/common/gotrue.ts:184` |
| **PostgREST** | Reached *through* pg-meta, not directly. The table editor's reads/writes are SQL over pg-meta; `PGRST_DB_SCHEMAS`/`PGRST_DB_MAX_ROWS` are passed to the meta service. | `turbo.jsonc:61-63`; `data/sql/execute-sql-mutation.ts:163-171` |
| **Logflare / Analytics (ClickHouse)** | `LOGFLARE_URL` (self-hosted, `:4000`) / the platform analytics endpoints | `.env:18`; `data/logs/execute-analytics-sql.ts:19-21` |
| **Storage API** | Through the platform API: `/platform/storage/{ref}/...` | `data/storage/buckets-query.ts:34-52` |
| **Realtime** | Not called by Studio's own data layer (the product exists in the stack; Studio's realtime UI is `components/interfaces/Realtime/`). | `docker/docker-compose.yml` service `realtime` |
| **Vector / S3 Vectors** | `/platform/storage/{ref}/vector-buckets/...` + `data/storage/vector-bucket-query.ts` | `data/storage/` listing |
| **Content API** | Snippets / notebooks: `NEXT_PUBLIC_CONTENT_API_URL`, `data/content/` | `turbo.jsonc:11`; `data/content/content-id-query.ts` |
| **Support API** | `NEXT_PUBLIC_SUPPORT_API_URL` | `turbo.jsonc:10` |
| **ConfigCat / PostHog** | `NEXT_PUBLIC_CONFIGCAT_SDK_KEY`, `NEXT_PUBLIC_POSTHOG_KEY` | `turbo.jsonc:20`; `packages/common/posthog-client.ts:77` |
| **Sentry** | `NEXT_PUBLIC_SENTRY_DSN` | `turbo.jsonc:91` |
| **Assistant LLM** | `OPENAI_API_KEY` / `@ai-sdk/amazon-bedrock` + `AWS_BEDROCK_*` | `turbo.jsonc:79,96-99` |

The self-hosted docker stack (`docker/docker-compose.yml`) contains: `studio`, `api-gw`, `auth`, `rest` (PostgREST), `realtime`, `storage`, `imgproxy`, `meta` (pg-meta), `functions`, `db`, `supavisor`, `db-config`, `deno-cache`.

### The scripted local-dev path (used by CI)

`package.json`:
```
setup:cli              → supabase start -x studio && supabase status --output json > keys.json && node scripts/generateLocalEnv.js
dev:studio-local       → pnpm setup:cli && NODE_ENV=test MODE=test pnpm --prefix ./apps/studio dev
e2e:setup:selfhosted   → SKIP_ASSET_UPLOAD=1 pnpm e2e:setup:cli && … pnpm run build:studio && … pnpm --prefix ./apps/studio start
```
`scripts/generateLocalEnv.js` writes `apps/studio/.env.test` from `keys.json` plus a fixed default block (`:12-42`), then writes `e2e/studio/.env.local` (`:60-71`).

### Docker

`apps/studio/Dockerfile`:
- `:16` `ARG STUDIO_FRAMEWORK=next` — framework is chosen at **image build time** (`build-next` vs `build-tanstack` stage, `:63-92`).
- `:104-107` production stage sets `PORT=3000`, exposes 3000.
- `:108` healthcheck hits `http://localhost:3000/api/platform/profile`.
- `:109` `CMD ["node", "apps/studio/server.js"]`.
- `apps/studio/docker-entrypoint.sh:23-25` supports Docker secrets via `*_FILE` for `POSTGRES_PASSWORD`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY`.

---

## Failure modes and gotchas

### 1. Two runtimes, one repo — an edit to `pages/**` can silently miss `routes/**`

**Symptom**: the page works under `pnpm dev` (Next) but 404s, renders unstyled, or loses its layout/`withAuth`/title under the TanStack build (or vice versa).

**Why**: `apps/studio/routes/project/$ref/editor/$id.tsx:3-11` re-exports the page's *default export* only. `getLayout` is "dropped on the floor" — the TanStack layout chain provides wrapping instead (`apps/studio/TANSTACK_MIGRATION.md:36-40`). `apps/studio/AGENTS.md:28` states you must mirror by hand only what the route duplicates: `getLayout`/layout wrapping, `staticData` (incl. `skip*Layout` flags), `withAuth`, or redirect paths.

**Also**: `apps/studio/AGENTS.md:27` — *"Never delete a page file."* Deleting a `pages/**` file breaks the Next build **and** the TanStack route.

### 2. Importing `next/*` in a Vite build without a shim → hard build failure

**Symptom**: the Vite build fails with `[next-compat] "next/xyz" imported from …` — "Add a shim under apps/studio/compat/next/ and register it in vite.config.ts, or use a framework-agnostic equivalent."

**Why**: `apps/studio/vite.config.ts:51-67` — the `nextCompat()` plugin resolves the 11 shimmed ids (`vite.config.ts:31-42`) and **throws for any other `next`/`next/*` import from app source**. This is deliberate: "we catch unshimmed usage at build time during the migration" (`vite.config.ts:44-50`).

### 3. Chunk-level circular imports → "X is not a function" at module load

**Symptom**: a page chunk crashes on load with `TypeError: c is not a function` / `"cva is not a function"` / `"e is not a function"` in `folder-open-<hash>.js`. Documented symptoms: `cva is not a function` during SSR prerender (`vite.config.ts:277-283`); `createLucideIcon` undefined → `TypeError: e is not a function` at `folder-open-<hash>.js` (`vite.config.ts:657-665`); `Alert-<hash>.js` crashing with `c is not a function` because `styleHandler` came from an over-large `lucide-react` chunk (`vite.config.ts:666-674`).

**Why**: Rolldown (Vite 8) pools a shared module into whichever page chunk happens to be its only non-barrel importer, while the `packages/ui` barrel re-exports it back — a cycle. The build now **fails** on new cycles: `assertNoChunkCycles()` (`vite.config.ts:305-371`) runs Tarjan's SCC over the emitted chunk graph and calls `this.error(...)` with the message *"detected N new chunk-level cycle(s) in the client bundle. These cause 'X is not a function' runtime errors at module-load time."* Workarounds are the `manualChunks` pins at `vite.config.ts:702-739` (`class-variance-authority`, `react-vendor`, `lucide-react`, `ui-field`, `ui-drawer`, `ui-form`, `ui-sidebar`, `ui-slider`).

### 4. SQL that is "too large" or "too expensive" — the error is a thrown string, not a 4xx

**Symptom**: the SQL editor shows *"Query is too large to be run via the SQL Editor"* for a query well under 1 MB (the check is on `Blob` byte size, not characters — `data/sql/execute-sql-mutation.ts:96-100` uses `0.98 * MB`), or *"Query cost exceeds threshold"* from a query that never ran.

**Why**: `:96-100` throws before the request; `:32-33` `COST_THRESHOLD = 200_000`; `:130-159` the `preflightCheck` path issues `explain <sql>` first and, on cost ≥ threshold, calls `handleErrorFetchers({message: COST_THRESHOLD_ERROR, code: cost, metadata:{cost, sql}})`. `preflightCheck` is only used by interfaces that lean heavily on the DB.

### 5. Logs/analytics SQL must pass the `safeSql` brand — a plain string will not compile

**Symptom**: TypeScript error at the call site, or (if forced) a runtime rejection of an unbranded string.

**Why**: `apps/studio/data/logs/execute-analytics-sql.ts:11,25-27` — the function accepts only `SafeLogSqlFragment`; "plain strings are rejected at compile time — so any value flowing from URL parameters, UI inputs, or LLM output must pass through a sanitization helper in safe-analytics-sql.ts before reaching the wire" (`:2-9`). Same idea for database SQL: `apps/studio/AGENTS.md:89` — "Ad-hoc SQL against the user's database goes through `executeSql` / `useExecuteSqlMutation`".

### 6. `useUser()` can throw on an unmigrated auth-js user proxy

**Symptom**: a crash (not a null) when reading any property of `session.user` right after login.

**Why**: `packages/common/auth.tsx:131-140` — auth-js substitutes a throwing proxy for `user` when `userStorage` is configured and the user has not been migrated into storage yet. The guard is `if (user && (user as any).__isUserNotAvailableProxy) return null`. Anyone re-implementing `useUser` locally loses this guard.

### 7. `withAuth` bounces you to `/sign-in-mfa` on a valid AAL1 session

**Symptom**: an SSO user lands on `/dashboard`, is immediately redirected to `/sign-in-mfa`, and the session is preserved (not signed out).

**Why**: `apps/studio/hooks/misc/withAuth.tsx:49` (`isAtHighestAAL = isSuccessAAL && aalData.currentLevel === aalData.nextLevel`), `:72-73`, `:89-95`. The platform API rejects sessions that have not completed the MFA challenge, so `useHighestAAL` defaults to `true` (`:17-26`). Also `:13` — if the AAL query itself never resolves, a `SessionTimeoutModal` opens after 10 s.

### 8. HTTP/3 empty-body responses → "Unexpected end of JSON input"

**Symptom**: a mutation succeeds over HTTP/2 but fails over HTTP/3 with a JSON parse error on an empty body (e.g. a `201` with no body).

**Why**: `apps/studio/data/fetchers.ts:67-106` — `openapi-fetch` only treats `status === 204` or `Content-Length: 0` as empty. `normalizeEmptyBodyResponse` re-wraps the response with a `Content-Length: 0` header.

### 9. Self-hosted: no auth at all, and a different API base

**Symptom**: on self-hosted, `withAuth` never redirects, `IS_PLATFORM` is false everywhere, and requests go to `/api` on the same origin rather than `api.supabase.com`.

**Why**: `apps/studio/hooks/misc/withAuth.tsx:29-31` (HOC is a no-op when `!IS_PLATFORM`); `apps/studio/lib/constants/index.ts:5` and `:35-46` (`API_URL` → `/api` in the browser). Practical consequence: platform-only queries must be gated — see `apps/studio/data/api-keys/legacy-api-keys-status-query.ts:38` (`enabled: IS_PLATFORM && …`).

### 10. React Query key invalidation after a SQL mutation is a heuristic

**Symptom**: after running DDL in the SQL editor, a table list or schema panel still shows stale data until a manual refresh.

**Why**: `apps/studio/data/sql/execute-sql-mutation.ts:24` — `INVALIDATION_KEYS_IGNORE = ['branches','settings-v2','addons','custom-domains','content']`; `:260-272` — invalidation only fires when `contextualInvalidation` is on, `projectRef` is set, and the SQL text contains `create `, `alter `, or `drop ` (naive substring match on the lowercased SQL). The comment at `:21-23` calls this out as hacky.

### 11. `vite dev --mode test` breaks every route

**Symptom**: every route 404s under `pnpm dev:tanstack` when `MODE=test`.

**Why**: `apps/studio/vite.config.ts:467-477` — "TanStack Start's dev-server plugin treats mode 'test' as 'running under vitest' and skips installing its SSR middleware entirely, so every route 404s". The dev path keeps mode `development` and emulates the `.env.test` cascade instead (`:484-489`).

### 12. `lodash` in SSR must be `lodash-es`, and `react-data-grid` is patched

**Symptom**: SSR crash *"is not a function"* for `lodash` named imports, or `ModuleJob._instantiate` failures for `react-use`.

**Why**: `apps/studio/vite.config.ts:240-251` — the CJS `lodash` evaluates as pure ESM in the dev module runner, so `isEqual` binds to `undefined` and only explodes when *called* during SSR. `vite.config.ts:783-789` `ssr.noExternal` lists `lodash`, `next/*`, `tslib` (build only), `react-use`, `awesome-debounce-promise`. `pnpm-workspace.yaml:133-134` patches `react-data-grid`.

### 13. The `ui` barrel creates chunk cycles — do not add new non-barrel importers

**Symptom**: a build failure from `studio-assert-no-chunk-cycles` naming a `packages/ui/src/components/shadcn/ui/*.tsx` file.

**Why**: `apps/studio/vite.config.ts:676-698` documents the pattern exactly — `field.tsx`, `drawer.tsx`, `form.tsx`, `sidebar.tsx`, `slider.tsx` each have exactly one non-barrel importer, so Rolldown pools them into that page's chunk while the `ui` barrel re-exports them back.

### 14. `api-types` is generated — do not hand-edit

**Symptom**: a type error after the OpenAPI spec changes upstream.

**Why**: `packages/api-types/package.json:11` — `"codegen": "openapi-typescript --redocly ./redocly.yaml --alphabetize …"`; `packages/api-types/types/{api-v1,api-v2,platform}.d.ts` are outputs. `apps/studio/data/api.d.ts:1-5` is a **deprecated** re-export shim: "Avoid importing this file and import the types directly from `api-types`".

---

## When to use this / when not to

**Use Studio as the reference when:**
- You are building a Supabase **dashboard/admin UI** on top of the platform API, pg-meta, or the content API. The `data/<domain>/` + `keys.ts` + `queryOptions` pattern is the house style, enforced by an LLM skill (`.agents/skills/studio-queries/SKILL.md`) and reviewed by humans.
- You need the **pg-meta SQL bridge**: Studio never opens a Postgres connection from the browser. It sends SQL to `/platform/pg-meta/{ref}/query` with an encrypted connection string. `packages/pg-meta` (147 files) holds the SQL builders and their Zod schemas. Use `getTableEditorSql`, `pgMeta.tables.list().sql`, `getTablesPaginatedSql`.
- You need a **worked example of dual-runtime migration**: `apps/studio/TANSTACK_MIGRATION.md` plus `apps/studio/vite.config.ts:31-67` (the `next/*` shim mechanism) is a rare, complete example of keeping Next pages router and TanStack Start alive in one app.
- You are writing a **Supabase-flavored React Query client** and want the error shape (`ResponseError` with `code`, `requestId`, `retryAfter`, `requestPathname`), the `handleError` contract, the `x-connection-encrypted` header convention, and the `safeSql`/`SafeLogSqlFragment` branding discipline.
- You want the **PostHog + first-party telemetry** pattern with consent gating, first-touch attribution, and `$feature/<key>` flag stamping.

**Do not use Studio as the reference when:**
- You want a **single-framework Next.js App Router example**. Studio is pages-router-first, only 4 files live in `app/`, and the App Router is not where the app lives.
- You want a **server-heavy or backend pattern**. Studio is a client-side SPA with a thin API-route layer (102 files in `pages/api/`); there is no ORM, no server actions, no BFF architecture. The heavy lifting is in `api-types` + `openapi-fetch`.
- You want **i18n, offline, or native-mobile** patterns. There is no i18n layer at all.
- You want a **lightweight setup**. Studio's build graph is enormous (5,605 files, 1,035 directories, two bundlers, 10 workspace packages, `knip` + lint-ratchet gates). It is a poor template for a small admin panel.
- You are **adding a new page**. Do not copy the Studio page pattern blindly: `apps/studio/AGENTS.md:29` — "A new page under `pages/**` needs a matching route under `routes/**` plus a checklist entry in `TANSTACK_MIGRATION.md`." The dual-file requirement is migration scaffolding that will be deleted.
- You want to **reuse the UI primitives**. `packages/ui` and `packages/ui-patterns` are internal, source-only workspace packages (`transpilePackages` at `apps/studio/next.config.ts:202`), with a shadcn/Radix base. Copying them means owning the Tailwind v4 theme in `apps/studio/styles/globals.css:10-30` and the `packages/ui` barrel that causes chunk cycles (`vite.config.ts:676-698`).

---

## Open questions

1. **Which runtime is the default in production today?** `apps/studio/AGENTS.md:25` says `STUDIO_FRAMEWORK` defaults to `next`, but `apps/studio/TANSTACK_MIGRATION.md:7-9` says "The Vite/TanStack build is what we run today; the Next build … stays alive as a fallback". These contradict. The Docker image defaults to `next` (`Dockerfile:16`), and CI runs both. **Not resolved from the repo.**
2. **Telemetry event catalogue size.** `packages/common/telemetry-constants.ts` holds the `TelemetryEvent` union; I did not count the entries. Not measured.
3. **Coverage expectations.** `apps/studio/vitest.config.ts:39-47` sets `include: ['lib/**/*.ts']` with no `thresholds`. No coverage gate exists in any workflow. Whether an unofficial target exists (e.g. Coveralls status check on `studio-tests`) is **not determinable from the repo** — the Coveralls upload is `continue-on-error: true` (`studio-unit-tests.yml:110`).
4. **`packages/api-types/types/*.d.ts` are generated from which OpenAPI source?** `packages/api-types/redocly.yaml` points somewhere; I did not trace the upstream spec URL or whether `platform.d.ts` is generated from the platform repo's spec. Not verified.
5. **PostgREST usage from Studio.** I found no direct PostgREST call from `apps/studio` — table reads/writes go through pg-meta SQL. Whether the platform's pg-meta internally uses PostgREST is **outside this repo**. Not verified.
6. **Realtime and Vector endpoints.** Studio's data layer has `data/storage/vector-bucket-query.ts` and `data/realtime/`, but I did not trace which backend serves them (platform proxy vs direct service). Not measured.
7. **The exact `enabled-features.json` feature count** in `packages/common/enabled-features/` was not counted.
8. **`e2e/studio` spec count.** I read `e2e/studio/playwright.config.ts` but did not count the `.spec.ts` files (the `e2e/studio/features/` tree was listed only partially). Not measured.
9. **Whether `packages/pg-meta` is the only SQL builder** — `apps/studio` also imports `libpg-query` (17.6.0) directly for parsing; I did not verify where that is used.
