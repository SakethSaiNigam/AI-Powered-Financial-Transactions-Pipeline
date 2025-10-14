# AI-Powered Financial Transactions Pipeline

A production-ready FastAPI service that ingests financial transactions at scale, flags anomalies,
and generates LLM-powered insights. Designed to process 1M+ transactions/day with async I/O,
SQLAlchemy 2.0, and optional background batching.

## Features
- **FastAPI** REST service (`/ingest`, `/transactions`, `/anomalies`, `/insights`)
- **PostgreSQL + SQLAlchemy 2.0** for durable storage
- **Anomaly detection**: statistical z-score + rules; optional **LLM risk reasoning** using OpenAI via LangChain
- **Async batching** for throughput; idempotent ingestion
- **Dockerized** with `docker-compose` (API + Postgres)
- **Config via env** with `.env` file
- **Tests** with pytest + httpx

> **Note:** LLM analysis is optional and disabled if no `OPENAI_API_KEY` is provided.

---

## Architecture
```
FastAPI --> /ingest --> DB (Postgres)
        \-> /analyze (background) --> Stats + (optional) LLM --> anomaly_score, reason
```

## Endpoints
- `POST /ingest` — ingest one or many transactions
- `GET /transactions` — list paginated transactions
- `GET /anomalies` — list flagged transactions (score >= threshold)
- `GET /insights/{transaction_id}` — return AI-generated rationale (if available)
- `POST /recompute` — recompute anomaly scores for a time range or all

## Quickstart (Local Python)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# copy env template and edit values
cp .env.example .env

# start the API
uvicorn app.main:app --reload

# Ingest sample data
python scripts/load_sample.py
```

Open the docs at: http://127.0.0.1:8000/docs

## Quickstart (Docker)
```bash
# 1) copy env template
cp .env.example .env

# 2) launch
docker compose up --build

# API: http://localhost:8000/docs
# DB: postgres:5432 (user: postgres, pass from env, db: transactions)
```

## Environment Variables (`.env`)
```
APP_ENV=dev
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/transactions
ANOMALY_Z_THRESHOLD=3.0
ANOMALY_AMOUNT_THRESHOLD=10000
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
ENABLE_LLM_ANALYSIS=false
BATCH_SIZE=1000
```

> For local without Docker, set `DATABASE_URL` like:
> `postgresql+psycopg2://postgres:postgres@localhost:5432/transactions`

## Project Structure
```
app/
  main.py
  config.py
  database.py
  models.py
  schemas.py
  routers/
    transactions.py
  services/
    anomaly.py
    insights.py
scripts/
  load_sample.py
tests/
  test_api.py
```

## Pushing to a New GitHub Repository
```bash
# Initialize git
git init
git add .
git commit -m "feat: initial commit - AI-powered transactions pipeline"

# Create a new repo on GitHub (via UI), then:
git branch -M main
git remote add origin https://github.com/<your-username>/ai-fin-transactions-pipeline.git
git push -u origin main
```

## Security Notes
- Never commit real secrets. Use `.env` and a secret manager (GitHub Actions, Azure Key Vault).
- Add IP allowlists and auth (e.g., API keys, OAuth) before production.
- LLM analysis should not leak PII. Mask / tokenize sensitive fields.

## License
MIT
