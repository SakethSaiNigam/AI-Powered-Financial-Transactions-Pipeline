from __future__ import annotations
from sqlalchemy.orm import Session
from typing import Iterable
import numpy as np
from app.config import settings
from app.models import Transaction

def compute_stats(amounts: np.ndarray) -> tuple[float, float]:
    if amounts.size == 0:
        return 0.0, 1.0
    mean = float(np.mean(amounts))
    std = float(np.std(amounts) or 1.0)
    return mean, std

def z_score(amount: float, mean: float, std: float) -> float:
    return abs(amount - mean) / std

def rule_based_flags(txn: Transaction) -> float:
    score = 0.0
    if abs(txn.amount) >= settings.anomaly_amount_threshold:
        score += 1.5
    if txn.category.lower() in {"crypto", "gambling"}:
        score += 0.75
    return score

def compute_anomaly_scores(db: Session, txns: Iterable[Transaction]) -> None:
    # stats by account
    from collections import defaultdict
    by_account = defaultdict(list)
    for t in txns:
        by_account[t.account_id].append(t.amount)

    stats = {acc: compute_stats(np.array(amts, dtype=float)) for acc, amts in by_account.items()}

    for t in txns:
        mean, std = stats.get(t.account_id, (0.0, 1.0))
        score = z_score(t.amount, mean, std) + rule_based_flags(t)
        t.anomaly_score = float(score)
        t.is_anomaly = bool(score >= settings.anomaly_z_threshold)

def summarize_for_llm(txn: Transaction) -> str:
    return (
        f"Transaction {txn.txn_id}: account={txn.account_id}, amount={txn.amount} {txn.currency}, "
        f"merchant='{txn.merchant}', category='{txn.category}', ts={txn.ts.isoformat()}"
    )
