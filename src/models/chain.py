"""RAG chain: embeddings, vector store, and QA chain."""
import logging
from pathlib import Path

from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_classic.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import (
    FAQ_CSV_PATH,
    FAISS_INDEX_DIR,
    LLM_MODEL,
    LLM_TEMPERATURE,
    RETRIEVER_TOP_K,
    get_google_api_key,
)
from src.data import load_faq_documents

logger = logging.getLogger(__name__)

# Prompt: answer from context only
QA_PROMPT_TEMPLATE = """This context is from a CSV file with questions and answers. You are a helpful assistant.
Answer the question using only the "response" part of the source document; do not change the wording.
If the answer is not in the documents, say "I don't know" and do not make up an answer.

CONTEXT: {context}

QUESTION: {question}"""


def _get_embeddings():
    """HuggingFace Instruct Embeddings (free, good quality)."""
    return HuggingFaceInstructEmbeddings()


def _get_llm():
    """Google Gemini LLM. API key is read when first needed."""
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        api_key=get_google_api_key(),
        temperature=LLM_TEMPERATURE,
    )


def create_vector_db(
    csv_path: Path = FAQ_CSV_PATH,
    index_dir: Path = FAISS_INDEX_DIR,
) -> None:
    """Build FAISS index from FAQ CSV and save to disk."""
    documents = load_faq_documents(csv_path)
    if not documents:
        raise ValueError("No documents loaded; CSV may be empty.")

    embeddings = _get_embeddings()
    vector_db = FAISS.from_documents(documents=documents, embedding=embeddings)
    index_dir = Path(index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    vector_db.save_local(str(index_dir))
    logger.info("Saved FAISS index to %s", index_dir)


def get_qa_chain(
    index_dir: Path = FAISS_INDEX_DIR,
    retriever_k: int = RETRIEVER_TOP_K,
):
    """Load FAISS index and return a RetrievalQA chain. Use invoke(question), not call()."""
    index_dir = Path(index_dir)
    if not index_dir.exists():
        raise FileNotFoundError(
            f"FAISS index not found at {index_dir}. Run: python main.py --build"
        )

    embeddings = _get_embeddings()
    # Loading from a path we control; allow_dangerous_deserialization needed for FAISS pickle
    vector_db = FAISS.load_local(
        str(index_dir),
        embeddings,
        allow_dangerous_deserialization=True,
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": retriever_k})

    prompt = PromptTemplate(
        template=QA_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )
    chain = RetrievalQA.from_chain_type(
        llm=_get_llm(),
        chain_type="stuff",
        retriever=retriever,
        input_key="query",
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain
