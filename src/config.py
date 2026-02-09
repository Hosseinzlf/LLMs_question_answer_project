"""Central configuration and env validation."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Paths (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAQ_CSV_PATH = PROJECT_ROOT / "codebasics_faqs.csv"
FAISS_INDEX_DIR = PROJECT_ROOT / "faiss_index"

# Data
CSV_SOURCE_COLUMN = "prompt"
CSV_ENCODING = "windows-1252"

# Model
LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.5
RETRIEVER_TOP_K = 4


def get_google_api_key() -> str:
    """Return Google API key; raise clear error if missing."""
    key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not key:
        raise ValueError(
            "GOOGLE_API_KEY is not set. "
            "Add it to a .env file or set the environment variable."
        )
    return key
