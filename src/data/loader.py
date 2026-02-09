"""Load and validate FAQ CSV data."""
import csv
import logging
from pathlib import Path

from langchain_community.document_loaders.csv_loader import CSVLoader

from src.config import CSV_ENCODING, CSV_SOURCE_COLUMN

logger = logging.getLogger(__name__)


def _validate_csv_columns(file_path: Path, required: str) -> None:
    """Ensure the CSV has the required column."""
    with open(file_path, encoding=CSV_ENCODING) as f:
        reader = csv.reader(f)
        header = next(reader, None)
    if not header or required not in header:
        raise ValueError(
            f"CSV must contain a '{required}' column. Found columns: {header or 'empty'}"
        )


def load_faq_documents(
    csv_path: Path,
    source_column: str = CSV_SOURCE_COLUMN,
    encoding: str = CSV_ENCODING,
):
    """Load FAQ documents from CSV. Validates required column exists."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"FAQ CSV not found: {csv_path}")

    _validate_csv_columns(csv_path, source_column)

    loader = CSVLoader(
        file_path=str(csv_path),
        source_column=source_column,
        encoding=encoding,
    )
    documents = loader.load()
    logger.info("Loaded %s documents from %s", len(documents), csv_path)
    return documents
