# OrderFlow frontend

A public crypto market dashboard built with Next.js App Router, React, TypeScript, Tailwind CSS v4, and Recharts. Visitors can view market performance, rolling volatility, and correlation charts without signing in. The frontend calls the public FastAPI API; the API reads market candles from PostgreSQL.

## Run locally

Use Node.js 20.9 or newer. From this `Frontend` directory:

```powershell
npm install
Copy-Item .env.local.example .env.local
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000). Set `NEXT_PUBLIC_API_URL` in `.env.local` if FastAPI is not at `http://localhost:8000`.

## Deployment configuration

Set `NEXT_PUBLIC_API_URL` to the deployed API's public HTTPS URL in the frontend hosting environment. Set the matching frontend URL in the backend's `CORS_ORIGINS`. The backend and PostgreSQL database must be deployed and populated with the `global_crypto_data` table for real charts to load. See [Backend/README.md](../Backend/README.md) for API configuration and table requirements.

The frontend contains no login flow or secrets. `NEXT_PUBLIC_API_URL` is public configuration, not a secret. Do not place database credentials in frontend environment variables.

## Pages and code

- `app/page.tsx` and `page.tsx` — landing page.
- `app/charts/page.tsx` — fetches public API data and renders charts.
- `app/layout.tsx` — shared HTML layout, header, and footer.
- `api.ts` — typed HTTP requests to FastAPI.
- `types.ts` — TypeScript interfaces for API data.
- `PctChangeLines.tsx`, `VolatilityChart.tsx`, and `CorrelationHeatmap.tsx` — chart components.

The API endpoints are public and can be called directly by anyone. CORS controls browser access; it is not authentication or a request quota. Keep database credentials on the backend, and consider rate limiting and query monitoring before traffic grows.

Useful commands: `npm run dev` starts development, `npm run typecheck` checks TypeScript, `npm run build` creates a production build, and `npm start` serves it.
