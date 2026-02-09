"""CLI: build FAISS index or run a demo query."""
import argparse
import logging
import sys

from src.config import get_google_api_key
from src.models import create_vector_db, get_qa_chain

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="FAQ RAG: build index or run a query.")
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build/rebuild FAISS index from CSV (run this after updating the FAQ CSV).",
    )
    parser.add_argument(
        "--query",
        default="Do you provide an internship?",
        help="Question to ask (used when not using --build).",
    )
    args = parser.parse_args()

    if args.build:
        try:
            get_google_api_key()  # fail fast if key missing
            create_vector_db()
            logger.info("Done. You can run the app or ask a query next.")
        except (ValueError, FileNotFoundError) as e:
            logger.error("%s", e)
            sys.exit(1)
        return

    # Default: run one query
    try:
        chain = get_qa_chain()
        out = chain.invoke(args.query)
        print("Answer:", out["result"])
    except (ValueError, FileNotFoundError) as e:
        logger.error("%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
