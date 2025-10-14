from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transactions

app = FastAPI(title="AI-Powered Financial Transactions Pipeline")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transactions.router)

@app.get("/health")
def health():
    return {"status": "ok"}
