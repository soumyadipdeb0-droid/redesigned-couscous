# Vercel-ready starter

This repository is set up as a simple static site that can be deployed on Vercel.

## What's included

- `index.html`: A minimal homepage.
- `vercel.json`: Deployment config that serves `index.html` at `/`.

## Run locally (quickest way to see output)

From the project root:

```bash
python3 -m http.server 4173
```

Then open:

- `http://localhost:4173`

You should see: **"✅ Vercel deployment is ready"**.

To stop the server, press `Ctrl+C`.

## Run locally with Vercel CLI (optional)

If you want to emulate Vercel routing/behavior locally:

```bash
npm i -g vercel
vercel login
vercel dev
```

Then open the local URL shown in your terminal (usually `http://localhost:3000`).

## Deploy on Vercel

### Option 1: Vercel dashboard (recommended)

1. Push this repo to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import the repository.
4. Keep default settings (Framework Preset: **Other**).
5. Click **Deploy**.

### Option 2: Vercel CLI

```bash
vercel
```

For production deployment:

```bash
vercel --prod
```

## Notes

- This is configured as a static project, so no build step is required.
- If you later add a framework (Next.js, Vite, etc.), update `vercel.json` or remove it and let Vercel auto-detect your framework.
