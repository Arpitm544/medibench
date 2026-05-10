from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "MediBench"
    VERSION: str = "0.1.0"
    APP_ENV: str = "development"
    DATABASE_URL: str = "sqlite:///./medibench.db"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    OPENAI_API_KEY: str = "mock-key"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"
    LOG_LEVEL: str = "INFO"

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    SAMPLES_DATA_DIR: Path = DATA_DIR / "samples"
    SQL_DIR: Path = BASE_DIR / "sql"
    REPORTS_DIR: Path = BASE_DIR / "reports"


settings = Settings()
