# GenAI FAQ assistant platform for Education-Tech

A context-aware Q&A app  over your FAQ data using LangChain, HuggingFace embeddings, Google Gemini, FAISS, and Streamlit.
 
---

## Features

- **FAQ RAG:** Answers from your CSV using retrieval + LLM.
- **Google Gemini & HuggingFace Instruct Embeddings**
- **FAISS** vector store for fast similarity search.
- **Streamlit** web UI; API key from `.env`.

---


## Installation

```bash
git clone <repo-url>
cd LLMs_question_answer_project
pip install -r requirements.txt
```

### API key

Create a `.env` file in the project folder:

```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

Or set the environment variable:

```bash
export GOOGLE_API_KEY=your_google_gemini_api_key_here
```

---

## Usage

### 1. FAQ data

- Put your FAQ CSV in the `data/` folder (e.g. `data/faqs.csv`).
- It must have a `prompt` column (questions) and a `response` column (answers).

### 2. Build the vector index

Run this **after adding or updating the CSV**:

```bash
python main.py --build
```

This creates the FAISS index in `faiss_index/`.

### 3. Ask a question (CLI)

```bash
python main.py --query "Do you provide an internship?"
```

### 4. Web app

```bash
streamlit run streamlit_webcode.py
```

- Use **Create / Rebuild Knowledge base** to rebuild the index from the CSV.
- Type a question to get an answer; source passages are shown in an expander.

---

## Project layout

- `data/` – FAQ CSV (e.g. `data/faqs.csv`)
- `src/config.py` – paths, model settings, env validation
- `src/data/` – load and validate FAQ CSV
- `src/models/` – create vector DB and QA chain
- `src/app/` – Streamlit UI
- `main.py` – CLI (`--build` or `--query`)
- `streamlit_webcode.py` – Streamlit entry point

---

## Development

From the project root (with dependencies installed):

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

## Security

- Do **not** commit `.env` or put the API key in code. Use environment variables or `.env` only.

## Tech stack

- [LangChain](https://python.langchain.com/)
- [HuggingFace Embeddings](https://huggingface.co/)
- [Google Gemini](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---


## Author

Hossein Zolfaghari – educational LLM project.

## License

Educational use.
