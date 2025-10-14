# AI-Powered-Financial-Transactions-Pipeline

# 💸 AI-Powered Financial Transactions Pipeline  
> Scalable backend service with real-time anomaly detection and LLM-driven insights

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-ready-0db7ed?logo=docker)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📘 Overview
This project is a **production-ready FastAPI service** that ingests, stores, and analyzes financial transactions at scale.  
It combines **statistical anomaly detection** with **AI-powered reasoning (OpenAI + LangChain)** to identify suspicious transactions and provide concise natural-language explanations.

The system is designed to handle **1M+ transactions per day** using asynchronous I/O and modern Python tooling.

---

## 🚀 Key Features

✅ **FastAPI REST API** — CRUD and analytics endpoints  
✅ **Scalable architecture** — PostgreSQL + SQLAlchemy 2.0  
✅ **Anomaly Detection** — z-score and rule-based hybrid  
✅ **LLM Integration (optional)** — OpenAI via LangChain for intelligent insights  
✅ **Dockerized Deployment** — ready for local or cloud (Azure / AWS / GCP)  
✅ **Real-time monitoring** — structured logs and API health checks  
✅ **Unit Tests** — pytest + httpx for async endpoint validation  

---

## 🏗️ Architecture

```text
+-------------+     +--------------------+     +---------------------+
| Client / UI | ---> | FastAPI Service   | ---> | PostgreSQL Database |
+-------------+       | • /ingest         |       | • transactions      |
| • /anomalies |      +-------------------+       +---------------------+
| • /insights (LLM) |
+--------------------+
          |
          v
+--------------------+
| OpenAI (LLM)       |
| LangChain Pipeline |
+--------------------+
```
---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| API Framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy 2.0 |
| Deployment | Docker & Docker Compose |
| ML/AI Layer | NumPy, OpenAI API, LangChain |
| DevOps | Uvicorn, pytest, dotenv |
| Language | Python 3.11 |

---

## 📂 Project Structure

```text
ai-fin-transactions-pipeline/
│
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment & settings
│   ├── database.py          # SQLAlchemy engine & session
│   ├── models.py            # ORM models
│   ├── schemas.py           # Pydantic models
│   ├── routers/
│   │   └── transactions.py  # API routes
│   └── services/
│       ├── anomaly.py       # z-score & rule-based detection
│       └── insights.py      # LLM reasoning (OpenAI)
│
├── scripts/
│   └── load_sample.py       # Generate & ingest test data
│
├── tests/
│   └── test_api.py          # Basic API test
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
---

## 🧪 Quickstart (Local Setup)

### 1️⃣ Clone and setup
```bash
git clone https://github.com/<your-username>/ai-fin-transactions-pipeline.git
cd ai-fin-transactions-pipeline

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```
---

### 2️⃣ Run the API
```bash
uvicorn app.main:app --reload
```
👉 Open http://127.0.0.1:8000/docs to explore the interactive Swagger UI.

🐳 Quickstart (Docker)
```bash
cp .env.example .env
docker compose up --build
```
API available at: http://localhost:8000/docs

Database: localhost:5432 (user: postgres / pass: postgres)

### 🔎 Core Endpoints
Method	Endpoint	Description
- POST	/ingest	Bulk ingest transactions
- GET	/transactions	List transactions (filter/pagination)
- GET	/anomalies	List high-risk anomalies
- GET	/insights/{transaction_id}	Fetch AI-generated reasoning
- POST	/recompute	Recalculate anomaly scores

### 🧰 Environment Variables
| Variable | Description | Default |
|-----------|--------------|----------|
| `APP_ENV` | Environment (dev/prod) | `dev` |
| `DATABASE_URL` | SQLAlchemy DB URI | `postgresql://postgres:postgres@db:5432/transactions` |
| `ANOMALY_Z_THRESHOLD` | Min score to flag anomalies | `3.0` |
| `ANOMALY_AMOUNT_THRESHOLD` | Rule-based high amount | `10000` |
| `OPENAI_API_KEY` | Your OpenAI key | *(empty)* |
| `OPENAI_MODEL` | Model for reasoning | `gpt-4o-mini` |
| `ENABLE_LLM_ANALYSIS` | Enable LLM risk reasoning | `false` |


### 💡 AI / LLM Integration
If **ENABLE_LLM_ANALYSIS=true** and **OPENAI_API_KEY** is provided, the service will automatically:
- Analyze flagged anomalies using OpenAI’s Chat Completions API
- Generate short natural-language rationales
- Cache reasoning results in the database

### 🧮 Testing
```bash
pytest -v
```

### ☁️ Deployment (Example)
Deploy easily to:
 - Azure Container Apps
 - AWS ECS / Fargate
 - Google Cloud Run
 - Render / Railway / Fly.io

Build and push image:
```bash
docker build -t your-username/ai-fin-transactions-pipeline .
docker push your-username/ai-fin-transactions-pipeline
```
### ✨ Author
**Saketh Sai Nigam Kanduri**
- 📧 kndrsakethms@gmail.com
- 🔗 [LinkedIn](www.linkedin.com/in/kandurisakethsainigam)
- 🎓 University College Dublin — M.Sc. Data & Computational Science
