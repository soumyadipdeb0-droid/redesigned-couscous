# Autonomous Job Search Agent (MVP)

A production-leaning Python MVP for an autonomous job-search workflow:

1. Parse resume into a structured candidate profile
2. Generate role/location search queries
3. Fetch jobs from providers (SerpAPI-ready + local mock provider)
4. Rank jobs by relevance (embedding-ready fallback scoring)
5. Deduplicate and persist to CSV
6. Build and send an email digest
7. Run manually or via scheduler/cron

## Project layout

```
job-agent/
├── agents/
│   ├── resume_agent.py
│   ├── search_agent.py
│   ├── ranking_agent.py
│   └── email_agent.py
├── utils/
│   ├── scraper.py
│   └── embeddings.py
├── data/
│   └── jobs.csv
├── config.json
├── main.py
└── scheduler.py
```

## Quick start

1. Create virtualenv and install dependencies
2. Copy `.env.example` to `.env` and set keys as needed
3. Run:

```bash
python main.py --resume sample_resume.txt --config config.json
```

For safe local testing, keep `provider: mock` in `config.json`.

## Environment variables

- `SERPAPI_API_KEY`: required when `provider: serpapi`
- `OPENAI_API_KEY`: optional for future LLM/embedding upgrades
- `SMTP_USERNAME`, `SMTP_PASSWORD`: for email sending

## Scheduling

Use `scheduler.py` with cron or OS task scheduler.

Example cron (9 AM daily):

```cron
0 9 * * * cd /path/to/repo && /usr/bin/python scheduler.py
```
