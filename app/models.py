from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Boolean, DateTime, JSON
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    txn_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    account_id: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(String(8), default="EUR")
    merchant: Mapped[str] = mapped_column(String(128), default="")
    category: Mapped[str] = mapped_column(String(64), default="")
    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    metadata: Mapped[dict | None] = mapped_column(JSON, default=None)

    # anomaly fields
    anomaly_score: Mapped[float] = mapped_column(Float, default=0.0, index=True)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    anomaly_reason: Mapped[str | None] = mapped_column(String(512), default=None)
