# Free deployment preparation

This project is prepared for a personal, non-commercial deployment using:

- Vercel Hobby for the Next.js frontend (root directory: `Frontend`).
- Render Free Web Service for FastAPI (configured in `render.yaml`).
- Neon Free PostgreSQL for the market database.

The API is public and read-only. CORS only controls browser-origin access; it does not stop scripts or other clients from calling the API.

## Free-tier tradeoffs

- Render's free web services sleep after 15 minutes without traffic and may take about a minute to wake. Render says its free services are for testing/hobby use, not production. See [Render free service limits](https://render.com/docs/free).
- Neon Free currently includes 1 GB storage and 100 CU-hours per project each month. Check the current [Neon plan limits](https://neon.com/pricing) against the actual candle database size and expected traffic before importing data.
- Vercel Hobby is for personal, non-commercial projects. If the app becomes commercial, check the [Vercel fair-use terms](https://vercel.com/docs/limits/fair-use-guidelines).

## Steps that require your provider accounts

1. Ensure the latest project is pushed to a Git provider that Vercel and Render can access. From `Frontend`, run `npm install`, then `npm run build`; commit the generated `Frontend/package-lock.json` so installs are reproducible. The current environment could not complete the package download, so the frontend build has not been verified here.
2. Create a Neon project in a region near the API host. Check that the database fits the free storage and usage quotas. Use Neon's pooled connection endpoint when available.
3. Import the existing PostgreSQL database into Neon. The API expects `global_crypto_data` and the columns listed in `Backend/README.md`; this project does not include an automatic schema/data migration.
4. In Render, create a Blueprint instance from this repository and `render.yaml`. Enter the Neon database host, database name, username, and password when prompted. Keep those values in Render's backend environment only. Set `CORS_ORIGINS` to a temporary value such as `["http://localhost:3000"]` for the first API deploy.
5. In Vercel, import the same repository, set the project root to `Frontend`, and add `NEXT_PUBLIC_API_URL` with the Render API's HTTPS URL. Deploy the frontend and copy its public origin, for example `https://your-project.vercel.app`.
6. Change Render's `CORS_ORIGINS` to the exact Vercel origin in JSON list form, such as `["https://your-project.vercel.app"]`, and redeploy the API.
7. Open the frontend and verify the charts show database data. Check the API's `/health` and `/docs` endpoints. Add a custom domain only if desired; DNS changes are done in the domain registrar.

## Manual actions

You need to create or sign in to the Vercel, Render, and Neon accounts; connect the Git repository; create the hosted database; transfer the data; enter database credentials into Render; deploy each service; and choose whether to add a domain. Provider account creation, billing choices, repository access, and database credentials must be handled in your provider accounts. Do not paste database passwords into frontend settings or commit them to Git.

If the database exceeds Neon's free quota, the API needs reliable always-on availability, or usage limits are too restrictive, choose a paid database/API plan or another provider before launch. Check provider pricing and quotas at deployment time because they can change.
