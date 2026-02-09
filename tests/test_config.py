"""Tests for config (paths and env)."""
from pathlib import Path

import pytest

from src.config import FAQ_CSV_PATH, FAISS_INDEX_DIR, PROJECT_ROOT, get_google_api_key


def test_project_root_is_directory():
    assert PROJECT_ROOT.is_dir()


def test_faq_csv_path_under_project_root():
    assert FAQ_CSV_PATH.relative_to(PROJECT_ROOT)
    assert FAQ_CSV_PATH.name == "codebasics_faqs.csv"


def test_faiss_index_dir_under_project_root():
    assert FAISS_INDEX_DIR.relative_to(PROJECT_ROOT)
    assert FAISS_INDEX_DIR.name == "faiss_index"


def test_get_google_api_key_raises_when_unset(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        get_google_api_key()


def test_get_google_api_key_raises_when_empty(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "   ")
    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        get_google_api_key()
