# OrderFlow frontend

A basic crypto charting dashboard built with Next.js App Router, React, TypeScript, Tailwind CSS v4, and Recharts. It has a landing page, admin sign-in, guest demo mode, and charts for relative performance, rolling volatility, and correlation.

## Start it

Use Node.js 20.9 or newer. In PowerShell, open this `Frontend` directory:

```powershell
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000). Set `NEXT_PUBLIC_API_URL` in `.env.local` if FastAPI is not at `http://localhost:8000`. Restart Next.js after changing the environment file.

To use real data, run FastAPI from the `Backend` folder, configure its `.env`, and make sure PostgreSQL contains the expected `global_crypto_data` table and data. Backend setup and table requirements are explained in [../Backend/README.md](../Backend/README.md). Use the configured admin username and the original password you hashed for the login screen. Or choose **Continue as guest**; the chart page then displays generated sample data and makes no API requests.

## What happens when you sign in

1. The login form calls `login()` in `api.ts`. It submits URL-encoded credentials to `POST /auth/login`, because the FastAPI endpoint uses `OAuth2PasswordRequestForm`.
2. FastAPI checks the configured admin credentials and returns a JWT bearer token. The frontend stores it in local storage through `AuthProvider.tsx`.
3. The charts page sends that token in an `Authorization: Bearer ...` header when requesting tickers, performance, volatility, and correlation.
4. FastAPI verifies token expiry/signature, reads PostgreSQL, computes analytics, validates the response with Pydantic models, and returns JSON.
5. Recharts turns the typed performance and volatility arrays into SVG charts. The correlation values are shown as a color heatmap.

The frontend origin and backend origin differ, so FastAPI's `CORS_ORIGINS` must include `http://localhost:3000`. A browser CORS error usually means this origin is missing or FastAPI was not restarted after changing it.

## Routes and folders

- `app/page.tsx` — landing page.
- `app/login/page.tsx` — sign-in form and guest entry.
- `app/charts/page.tsx` — dashboard data loading and charts.
- `app/layout.tsx` — shared HTML layout, header, footer, and auth context.
- `api.ts` — typed HTTP requests to FastAPI.
- `types.ts` — TypeScript interfaces matching API data.
- `AuthProvider.tsx` — login state, token storage, guest state, and logout.
- `PctChangeLines.tsx`, `VolatilityChart.tsx`, `CorrelationHeatmap.tsx` — reusable chart views.
- `mockData.ts` — generated guest-only demo values.

In Next.js App Router, a folder under `app` becomes part of the URL and its `page.tsx` file renders that route. The root layout wraps all pages so the header and authentication state are shared.

## API configuration and guest limitations

`NEXT_PUBLIC_API_URL` is intentionally public: it is compiled into browser code and is not a place for secrets. The database password, JWT key, and admin password hash belong only in the backend `.env`. This project has a single backend-configured admin identity, not public account registration. Guest mode is a frontend demo state and its generated data is not market data.

The JWT is kept in local storage for this learning/demo application. For a production app with sensitive user data, prefer a backend-managed secure, httpOnly cookie session and add appropriate account management and security controls.

## Changing or extending the app

- Change page styling in `globals.css` and Tailwind classes.
- Change API response shapes in `types.ts` when the backend schemas change; update `api.ts` and the chart page as needed.
- Add a page by creating `app/your-route/page.tsx`.
- Add an endpoint in FastAPI and a corresponding typed request function in `api.ts`.
- Update the supported navigation links in `Header.tsx`.

Useful commands: `npm run dev` starts the development server, `npm run build` makes a production build, and `npm start` serves that build. The frontend and backend are separate processes and both need to be running for signed-in real data.
