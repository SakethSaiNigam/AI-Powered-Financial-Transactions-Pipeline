from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from typing import List
from datetime import datetime
from app.database import get_db, Base, engine
from app.models import Transaction
from app.schemas import IngestRequest, TransactionOut, RecomputeRequest
from app.services.anomaly import compute_anomaly_scores
from app.services.insights import llm_reason_for_transaction

router = APIRouter()

# Ensure tables are created at import time (simple demo alternative to Alembic)
Base.metadata.create_all(bind=engine)

@router.post("/ingest", response_model=List[TransactionOut])
def ingest(payload: IngestRequest, db: Session = Depends(get_db)):
    # Idempotent insert: skip if txn_id exists
    created: list[Transaction] = []
    for t in payload.transactions:
        existing = db.scalar(select(Transaction).where(Transaction.txn_id == t.txn_id))
        if existing:
            created.append(existing)
            continue
        obj = Transaction(
            txn_id=t.txn_id,
            account_id=t.account_id,
            amount=t.amount,
            currency=t.currency,
            merchant=t.merchant,
            category=t.category,
            ts=t.ts,
            metadata=t.metadata,
        )
        db.add(obj)
        created.append(obj)

    db.flush()  # assign ids

    # Compute anomaly scores for the batch
    compute_anomaly_scores(db, created)

    # Optional LLM reason for anomalous ones
    for obj in created:
        if obj.is_anomaly:
            obj.anomaly_reason = llm_reason_for_transaction(obj) or obj.anomaly_reason

    db.commit()
    return created

@router.get("/transactions", response_model=List[TransactionOut])
def list_transactions(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    account_id: str | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Transaction).order_by(Transaction.ts.desc()).offset(offset).limit(limit)
    if account_id:
        stmt = select(Transaction).where(Transaction.account_id == account_id).order_by(Transaction.ts.desc()).offset(offset).limit(limit)
    rows = db.scalars(stmt).all()
    return rows

@router.get("/anomalies", response_model=List[TransactionOut])
def list_anomalies(
    min_score: float = Query(3.0, ge=0.0),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Transaction)
        .where(Transaction.anomaly_score >= min_score)
        .order_by(Transaction.anomaly_score.desc())
        .offset(offset).limit(limit)
    )
    rows = db.scalars(stmt).all()
    return rows

@router.get("/insights/{transaction_id}", response_model=TransactionOut)
def get_insights(transaction_id: int, db: Session = Depends(get_db)):
    txn = db.get(Transaction, transaction_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Transaction not found")
    # If not present, try to compute on-demand
    if txn.is_anomaly and not txn.anomaly_reason:
        reason = llm_reason_for_transaction(txn)
        if reason:
            txn.anomaly_reason = reason
            db.commit()
            db.refresh(txn)
    return txn

@router.post("/recompute")
def recompute(req: RecomputeRequest, db: Session = Depends(get_db)):
    stmt = select(Transaction)
    if req.from_ts and req.to_ts:
        stmt = stmt.where(and_(Transaction.ts >= req.from_ts, Transaction.ts <= req.to_ts))
    rows = db.scalars(stmt).all()
    compute_anomaly_scores(db, rows)
    db.commit()
    return {"recomputed": len(rows)}
