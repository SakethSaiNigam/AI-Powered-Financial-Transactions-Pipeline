from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/transactions")
    anomaly_z_threshold: float = float(os.getenv("ANOMALY_Z_THRESHOLD", "3.0"))
    anomaly_amount_threshold: float = float(os.getenv("ANOMALY_AMOUNT_THRESHOLD", "10000"))
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    enable_llm_analysis: bool = os.getenv("ENABLE_LLM_ANALYSIS", "false").lower() == "true"
    batch_size: int = int(os.getenv("BATCH_SIZE", "1000"))

settings = Settings()
