# Calling CRM

Screenshot-inspired CRM dashboard with institute management, call queue, staff, reports, CSV import and settings.

## Run locally

Open `dist/index.html` in a browser, or serve the `dist` folder with any static server.

## Deploy on Vercel

1. Push this folder to a GitHub repository.
2. Import that repository in Vercel.
3. Set the Output Directory to `dist` and deploy.

## Connect Supabase

1. Open Supabase SQL Editor and run `supabase-schema.sql`.
2. Add Supabase authentication and environment variables before using real customer data.
3. Never put the Supabase service-role key in browser code. Only the public anon key may be used client-side.

The current frontend uses sample data so it can be previewed immediately. The included SQL defines the production-ready data structure for the next integration step.
