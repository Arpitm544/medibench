import logging

import pandas as pd
from sqlalchemy import text

from medibench.config import settings
from medibench.database import engine
from medibench.validation.schema import COLUMN_MAPPING

logger = logging.getLogger(__name__)


def clean_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes column names, handles '?' missing values, and adds derived analytical flags.
    Preserves all records.
    """
    df = raw_df.rename(columns=COLUMN_MAPPING).copy()

    # Replace '?' with None across entire dataframe
    df = df.replace("?", None)

    # Derived boolean flags
    df["readmitted_30d"] = df["readmitted"] == "<30"
    df["readmitted_any"] = df["readmitted"].isin(["<30", ">30"])

    return df


def load_dataset_to_db(df: pd.DataFrame, batch_size: int = 10000, if_exists: str = "replace") -> int:
    """
    Loads DataFrame into patient_encounters table efficiently.
    """
    settings.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    clean_csv = settings.PROCESSED_DATA_DIR / "diabetic_data_clean.csv"
    clean_parquet = settings.PROCESSED_DATA_DIR / "diabetic_data_clean.parquet"

    # Save processed artifacts
    df.to_csv(clean_csv, index=False)
    try:
        df.to_parquet(clean_parquet, index=False)
    except Exception as e:
        logger.warning(f"Could not write parquet: {e}")

    logger.info(f"Loading {len(df)} records into 'patient_encounters'...")

    # Write to database using engine
    with engine.begin() as conn:
        if if_exists == "replace":
            conn.execute(text("DELETE FROM patient_encounters;"))

    df.to_sql(
        "patient_encounters",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=2000,
        method=None,
    )

    logger.info(f"Successfully loaded {len(df)} records into database.")
    return len(df)
