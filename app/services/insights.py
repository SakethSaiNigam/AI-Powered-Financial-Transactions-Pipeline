from __future__ import annotations
from app.config import settings
from app.models import Transaction

# Lazy import to avoid hard dependency if key not provided
def _get_client():
    if not settings.enable_llm_analysis or not settings.openai_api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=settings.openai_api_key)
    except Exception:
        return None

SYSTEM_PROMPT = (    "You are a risk analyst AI. Given a transaction, assess if it's anomalous or risky. "
    "Explain briefly (<=60 words) citing specific details like unusual amount, merchant, time, or category. "
    "Output: 'risk: <low|medium|high>; reason: <short explanation>'"
)

def llm_reason_for_transaction(txn: Transaction) -> str | None:
    client = _get_client()
    if not client:
        return None
    user_msg = (
        f"Assess risk for: id={txn.txn_id}, account={txn.account_id}, amount={txn.amount} {txn.currency}, "
        f"merchant='{txn.merchant}', category='{txn.category}', timestamp='{txn.ts.isoformat()}'"
    )
    try:
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.2,
            max_tokens=120,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None
