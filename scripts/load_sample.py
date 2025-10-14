import os, random, uuid
from datetime import datetime, timedelta
import httpx

API = os.getenv("API", "http://127.0.0.1:8000")
N = int(os.getenv("N", "5000"))
ACCOUNTS = [f"ACC-{i:04d}" for i in range(1, 51)]
CATEGORIES = ["retail", "groceries", "fuel", "travel", "utilities", "crypto", "gambling", "services"]
MERCHANTS = ["Contoso", "Fabrikam", "Tailwind", "Northwind", "BlueYonder"]

def gen_txn(i):
    account = random.choice(ACCOUNTS)
    # base amount distribution
    base = random.gauss(80, 30)
    # inject anomalies
    if random.random() < 0.02:
        base *= random.randint(50, 200)
        cat = random.choice(["crypto", "gambling"])
    else:
        cat = random.choice(CATEGORIES)
    return {
        "txn_id": str(uuid.uuid4()),
        "account_id": account,
        "amount": round(abs(base), 2),
        "currency": "EUR",
        "merchant": random.choice(MERCHANTS),
        "category": cat,
        "ts": (datetime.utcnow() - timedelta(minutes=random.randint(0, 60*24))).isoformat(),
        "metadata": {"source": "generator", "i": i},
    }

def main():
    txns = [gen_txn(i) for i in range(N)]
    print(f"Ingesting {N} sample transactions to {API} ...")
    with httpx.Client(timeout=30.0) as client:
        # send in chunks
        BATCH = 500
        for i in range(0, N, BATCH):
            chunk = txns[i:i+BATCH]
            r = client.post(f"{API}/ingest", json={"transactions": chunk})
            r.raise_for_status()
            print(f"  -> {i+len(chunk)}/{N}")

if __name__ == "__main__":
    main()
