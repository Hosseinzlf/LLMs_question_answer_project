"""Tests for data loading."""
from pathlib import Path

import pytest

from src.config import PROJECT_ROOT
from src.data import load_faq_documents


def test_load_faq_documents_returns_list():
    csv_path = PROJECT_ROOT / "codebasics_faqs.csv"
    if not csv_path.exists():
        pytest.skip("FAQ CSV not in project root")
    docs = load_faq_documents(csv_path)
    assert isinstance(docs, list)
    assert len(docs) > 0


def test_load_faq_documents_raises_on_missing_file():
    with pytest.raises(FileNotFoundError, match="not found"):
        load_faq_documents(PROJECT_ROOT / "nonexistent.csv")


def test_load_faq_documents_raises_on_missing_column(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("wrong_column,other\nrow1,row2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="prompt"):
        load_faq_documents(bad_csv)
