from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TransactionIn(BaseModel):
    txn_id: str = Field(..., description="Idempotency key for the transaction")
    account_id: str
    amount: float
    currency: str = "EUR"
    merchant: str = ""
    category: str = ""
    ts: datetime
    metadata: dict | None = None

class TransactionOut(BaseModel):
    id: int
    txn_id: str
    account_id: str
    amount: float
    currency: str
    merchant: str
    category: str
    ts: datetime
    anomaly_score: float
    is_anomaly: bool
    anomaly_reason: Optional[str] = None

    class Config:
        from_attributes = True

class IngestRequest(BaseModel):
    transactions: List[TransactionIn]

class RecomputeRequest(BaseModel):
    from_ts: datetime | None = None
    to_ts: datetime | None = None
