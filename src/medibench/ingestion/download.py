import hashlib
import io
import logging
import zipfile
from pathlib import Path

import requests

from medibench.config import settings

logger = logging.getLogger(__name__)

UCI_DATASET_URL = "https://archive.ics.uci.edu/static/public/296/diabetes+130-us+hospitals+for+years+1999-2008.zip"


def calculate_sha256(filepath: Path) -> str:
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_dataset(force: bool = False) -> tuple[Path, str]:
    """
    Downloads and extracts the Diabetes 130-US Hospitals dataset (101,766 records)
    from the UCI repository to data/raw/.
    """
    settings.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    target_csv = settings.RAW_DATA_DIR / "diabetic_data.csv"
    settings.RAW_DATA_DIR / "IDS_mapping.csv"

    if target_csv.exists() and not force:
        checksum = calculate_sha256(target_csv)
        logger.info(f"Dataset already exists at {target_csv} with SHA256: {checksum}")
        return target_csv, checksum

    logger.info(f"Downloading dataset from {UCI_DATASET_URL}...")
    response = requests.get(UCI_DATASET_URL, timeout=60)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        for filename in z.namelist():
            if filename.endswith(".csv"):
                extracted_path = z.extract(filename, settings.RAW_DATA_DIR)
                logger.info(f"Extracted: {extracted_path}")

    if not target_csv.exists():
        raise FileNotFoundError(f"Expected {target_csv} not found after extraction")

    checksum = calculate_sha256(target_csv)
    logger.info(f"Download complete. SHA256: {checksum}")
    return target_csv, checksum


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_dataset()
