# Zolfaghari QA Website

A professional, context-aware Question & Answer web application leveraging state-of-the-art Large Language Models (LLMs) and vector search. Built using LangChain, HuggingFace embeddings, Google Gemini, FAISS, and Streamlit.

---

## 🚀 Features

- **LLM-Powered Q&A:** Answers questions based on your own FAQ database.
- **Google Gemini & HuggingFace Instruct Embeddings:** Ensures high accuracy and robust language understanding.
- **FAISS VectorStore:** Efficient and scalable vector search on your document embeddings.
- **Streamlit Web App:** Simple, elegant, interactive web interface.
- **Secure API Key Management:** API keys loaded from environment variables or `.env` file.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repo-url>
cd questionproject/LLMs_question_answer_project
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

You need a Google Generative AI API key.

- **Using `.env` file:**  
  Create a file named `.env` in the project folder with:
  ```
  GOOGLE_API_KEY=your_google_gemini_api_key_here
  ```
  The script will automatically load this file.

- **OR set environment variable manually:**  
  ```bash
  export GOOGLE_API_KEY=your_google_gemini_api_key_here
  ```

---

## 📁 Usage

### 1. **Prepare FAQ Data:**
- Place your FAQ CSV (e.g., `codebasics_faqs.csv`) in the project folder.
- The CSV should contain at least a `prompt` column (questions) and a `response` column (answers).

### 2. **Build Vector Database**

Run (optional, only if you add/update the CSV):
```bash
python main.py
```
This creates or updates the FAISS vector store from your CSV.

### 3. **Launch Web App**

```bash
streamlit run streamlit_webcode.py
```
Open the provided local URL in your browser.

---

## 📝 Example

- Enter your question in the input box.
- The app provides the most contextually relevant answer based on your FAQ CSV.

---

## 🗝️ Security Note

- Your API key should **never** be hard-coded in scripts. Use environment variables or `.env`.
- The vector store uses Pickle format. Only use `allow_dangerous_deserialization=True` if you completely trust the `.pkl` files you load.

---

## 📚 Technologies Used

- [LangChain](https://python.langchain.com/)
- [HuggingFace Embeddings](https://huggingface.co/)
- [Google Gemini (Generative AI)](https://ai.google.dev/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Streamlit](https://streamlit.io/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---

## 👨‍💻 Authors

- Developed by Hossein Zolfaghari
- For educational and hands-on LLM projects

---

## 📄 License

This project is for educational purposes.
