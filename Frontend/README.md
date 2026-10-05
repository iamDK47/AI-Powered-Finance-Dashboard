# OrderFlow — Crypto Dashboard Frontend

Next.js 16 + TypeScript + Tailwind v4. Builds clean, type-checks clean, and
every route was verified to actually serve real content before this was
handed to you — see "What was actually tested" at the bottom.

## Run it

```bash
npm install
cp .env.local.example .env.local
npm run dev
```

Visit `http://localhost:3000`. `NEXT_PUBLIC_API_URL` in `.env.local` should
point at your FastAPI backend (defaults to `http://localhost:8000`, matching
the backend project from earlier).

Log in with the admin credentials you set up in the FastAPI backend's
`.env`, or click "Continue as guest" to browse with sample data — no
backend required for that path at all.

---

## Why Next.js instead of plain React

Not marketing, specific mechanisms this project actually uses:

- **File-based routing.** `/app/charts/page.tsx` existing as a file IS the
  `/charts` route — no router library to configure, no route table to keep
  in sync with your folder structure. Add `app/portfolio/page.tsx` and
  `/portfolio` exists, full stop.
- **Server Components by default.** `app/docs/page.tsx` and
  `app/about/page.tsx` have no `"use client"` directive — they render to
  HTML on the server with zero JavaScript shipped to the browser for those
  pages. Pages that actually need interactivity (`charts`, `login`,
  `insights`) opt into client-side JS explicitly. Plain React ships as a
  client-side bundle by default; you'd have to reach for a separate
  framework (or roll your own SSR) to get this split at all.
- **Environment variable conventions.** The `NEXT_PUBLIC_` prefix
  distinguishing browser-exposed vars from server-only ones is a Next.js
  convention, not a plain-React one — Vite/CRA each have their own
  different prefix rules.
- **Where plain React (e.g. Vite) would genuinely be the better call:** a
  purely client-rendered internal tool with no SEO need and no server
  rendering benefit. This dashboard leans on Next.js mostly for the routing
  and project-structure conventions, not deep SSR usage — worth being
  honest that Vite+React would work fine here too. Next.js is the pick
  because it's the more common expectation in job postings and interviews,
  not because this specific app has no alternative.

## Why TypeScript instead of JavaScript

Concrete instances already caught real mistakes while building this:

- `lib/types.ts` defines `Kline`, `PctChangePoint`, etc. once. Every
  component that touches this data gets autocomplete and a compile error
  if a field is misspelled or a shape doesn't match — in plain JS, a typo
  like `data.markte_buy_volume` fails silently at runtime, often deep
  inside a chart render, far from where the actual mistake was made.
  In TS it's a red squiggly line before you even save the file.
- The production build (`npm run build`) runs a full TypeScript check and
  refuses to ship if types don't line up — this caught a real bug during
  development (a recharts prop typed more loosely than I'd assumed) before
  it ever reached a browser.
- Cost, to be honest about the trade-off: every new data shape needs an
  `interface` written up front, which is real extra upfront syntax
  compared to JS. For a solo project the payoff is smaller than on a team,
  but TypeScript is close to a baseline expectation in professional
  codebases now — worth the habit regardless.

---

## Design decisions — what I chose, and the alternatives

You asked for the alternatives to be named explicitly, not just the final
choice. Four real decisions in this codebase:

**1. Auth token storage: localStorage vs httpOnly cookie**
Chosen: localStorage, via `AuthProvider.tsx`. Why: the FastAPI backend
returns the JWT in the response body and expects it back in an
`Authorization: Bearer` header — that pairs naturally with localStorage.
The alternative (httpOnly cookie) is more secure against XSS-based token
theft, but requires the backend to set/read cookies instead of a bearer
header, and the frontend to send `credentials: "include"` — a coordinated
change on both sides, not a frontend-only swap. Worth doing if this ever
handles real user funds or sensitive data; not worth the complexity for a
personal analytics dashboard today.

**2. Where correlation/volatility are computed: browser vs backend**
Chosen: browser, in `lib/analytics.ts`, from raw klines the existing
`/klines` endpoint already returns. Why: this works TODAY against the
backend you already have, with zero new backend code. The better long-term
architecture is a backend endpoint (`GET /analytics/correlation`, say) that
does this with pandas server-side and ships back a small pre-computed
payload instead of raw rows — that's a better fit for the `analysis.py`
work already planned for the pipeline, and avoids pulling thousands of raw
rows into the browser just to collapse them to ~30 daily points. `lib/analytics.ts`
has a comment at the top marking exactly this as the upgrade path.

**3. Guest mode scope: fully blocked vs demo data**
Chosen: guests see every page, with mock/sample data standing in on
`Charts` and `Insights` (real backend calls are skipped entirely for
guests — see the `isGuest` branches in those two pages). Why: a fully
blocked "sign in to see anything" wall is a worse first impression for
anyone evaluating this as a portfolio piece — letting them see the actual
UI working, even with fake numbers, sells the build better than a login
wall. The alternative — hard-gating Charts/Insights entirely behind
`middleware.ts` — is the right call if this ever becomes a real product
with a genuine free/paid split; noted as the option, not built, since it's
not needed yet.

**4. "AI analytics": real feature vs honest placeholder**
Chosen: honest placeholder. The "General insights" section on `/insights`
IS real — actual computed correlation/volatility numbers turned into
sentences, no LLM involved. The "AI analytics" input box below it is
visibly disabled with a tooltip explaining why, rather than faking a
response. Wiring it up for real means a backend route that feeds the
computed stats plus the user's question to an LLM API — a real, buildable
feature, just not one to fake in a scaffold.

---

## Where to edit things

| Want to change... | Edit this |
|---|---|
| Any color in the whole app | `app/globals.css` — the `:root` block. Every component uses Tailwind classes like `bg-surface`/`text-accent` that read from here; nothing is hardcoded elsewhere **except** `lib/chartColors.ts`, which duplicates the palette as literal hex values because chart libraries need real color strings, not CSS classes — keep both in sync by hand. |
| Header links (add/remove/reorder pages) | `components/Header.tsx` — the `NAV_LINKS` array at the top. The nav renders directly from this list. |
| Which tickers are selectable on Charts | `app/charts/page.tsx` — the `AVAILABLE_TICKERS` array. |
| Footer details | `components/Footer.tsx` — the `FOOTER_DETAILS` object at the top. |
| Add a new chart type | Add a component in `components/charts/`, following the pattern in the existing three (props in, `ResponsiveContainer` + recharts element out), then import and place it in `app/charts/page.tsx`. |
| Add a new page | Create `app/your-page/page.tsx`, add an entry to `NAV_LINKS` in `Header.tsx` if it should appear in the nav. |
| Dashboard copy | `app/page.tsx` — the hero text and the three feature cards are plain strings/objects, no logic to work around. |
| Market docs content | `app/docs/page.tsx` — the `DOCS` array. Add/remove/rewrite entries freely. |

---

## Authentication — current state and how to scale it

Right now: one hardcoded admin identity, checked against env vars on the
backend (see the FastAPI project's README). The frontend doesn't know or
care that it's "single-admin" — it just calls `POST /auth/login` and
stores whatever token comes back. That's the important property: **when
you add real multi-user auth, this frontend needs zero changes.** The
backend swaps a hardcoded check for a database lookup; the login flow,
token storage, and every protected fetch call here stay identical.

**Guest users** are handled entirely on the frontend, in
`AuthProvider.tsx` — `continueAsGuest()` sets a flag, no backend call at
all. Pages branch on `isGuest` to show mock data (`lib/mockData.ts`)
instead of calling the real API. When you're ready to support real guest
*accounts* (rate-limited real data instead of fake data, say), that's a
backend concern — an unauthenticated or anonymous-token endpoint — the
frontend's guest branch would just point at real (if limited) data instead
of the mock generator.

**Scaling to multiple real users**, when that day comes: add a `users`
table on the backend, replace the hardcoded credential check in
`auth.py`'s login route with a database lookup, done. Nothing here changes.

---

## Common edge cases handled (and a few deliberately not)

**Handled:**
- Hydration mismatch — `AuthProvider` reads `localStorage` only inside
  `useEffect`, never during render, with an `isLoading` flag so consumers
  can wait for the real auth state instead of flashing "logged out" first.
- Expired/invalid token — `lib/api.ts` throws a distinct `"UNAUTHORIZED"`
  error on a 401; `app/charts/page.tsx` catches it specifically and logs
  the user out + redirects to `/login`, instead of showing a raw error on
  a broken page.
- Empty ticker selection, loading state, and fetch-failure state are all
  distinct UI states on the Charts page — never a blank page with no
  explanation.
- Responsive layout — header collapses to a hamburger menu below the `md`
  breakpoint; the correlation heatmap scrolls horizontally instead of
  squashing illegibly on narrow screens.
- Build-time reliability — no external font fetch at build time (see the
  Next.js-vs-React section's font note), so `npm run build` can't fail
  because Google's font CDN had a bad moment or a firewall blocked it.

**Deliberately not handled yet (real scope decisions, not oversights):**
- No token refresh flow — the JWT just expires and the user re-logs-in.
  Fine for a personal dashboard; a refresh-token flow is the real answer
  once session length actually matters to users.
- No retry/backoff on failed API calls — one failure shows the error state
  immediately. Worth adding if the backend becomes flaky in practice.
- No pagination on the klines fetch — `limit: 2000` is hardcoded in the
  Charts/Insights fetch calls. Fine at current data volumes; would need
  real pagination if you start requesting much longer date ranges.

---

## Connecting to the FastAPI backend

1. Backend running on `http://localhost:8000` (or wherever
   `NEXT_PUBLIC_API_URL` points).
2. CORS: the backend's `cors_origins` setting must include this app's
   origin (`http://localhost:3000` by default — already the FastAPI
   backend's default, so local dev needs no changes on either side).
3. Every authenticated fetch here sends `Authorization: Bearer <token>` —
   matches exactly what the backend's `get_current_user` dependency
   expects.
4. The `/klines` endpoint returns raw rows for ONE ticker at a time — the
   Charts and Insights pages fetch each selected ticker separately (in
   parallel, via `Promise.all`) and combine them client-side. If you add
   a multi-ticker backend endpoint later, that's a change to
   `lib/api.ts` and the fetch calls in those two pages — the chart
   components themselves wouldn't need to change, since they only consume
   the already-shaped `PctChangePoint[]` / `VolatilityPoint[]` /
   `CorrelationMatrix` types regardless of where the data came from.

---

## What was actually tested before this was handed to you

- `npm run build` — full production build, TypeScript strict-mode check,
  and static generation for all 7 routes. Caught and fixed 3 real bugs in
  the process (a wrong import path, a build-time external font
  dependency, and a recharts type mismatch).
- Production server actually started and every route was curled to
  confirm real expected content renders — not just that the build
  succeeded, but that each page serves what it's supposed to.

What this does NOT verify: real backend integration (no live Postgres in
the environment this was built in), and no browser-level check for
console warnings or visual layout issues — worth a manual look once it's
running on your machine.
