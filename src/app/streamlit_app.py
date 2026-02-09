"""Streamlit UI for FAQ Q&A."""
import streamlit as st

from src.config import FAISS_INDEX_DIR
from src.models import create_vector_db, get_qa_chain


def main():
    st.set_page_config(page_title="Zolfaghari QA", page_icon="❓")
    st.title("Zolfaghari QA")

    @st.cache_resource
    def _load_chain():
        return get_qa_chain(index_dir=FAISS_INDEX_DIR)

    if st.button("Create / Rebuild Knowledge base"):
        with st.spinner("Building index from CSV…"):
            try:
                create_vector_db()
                st.success("Knowledge base created. You can ask questions below.")
            except Exception as e:
                st.error(f"Failed to build index: {e}")

    question = st.text_input("Question:").strip()

    if question:
        with st.spinner("Searching and generating answer…"):
            try:
                chain = _load_chain()
                response = chain.invoke(question)
                st.header("Answer")
                st.write(response["result"])
                if response.get("source_documents"):
                    with st.expander("Source passages"):
                        for i, doc in enumerate(response["source_documents"][:3], 1):
                            st.caption(f"Passage {i}")
                            st.text(
                                doc.page_content[:500]
                                + ("…" if len(doc.page_content) > 500 else "")
                            )
            except FileNotFoundError:
                st.warning(
                    "Knowledge base not found. Click **Create / Rebuild Knowledge base** first."
                )
            except Exception as e:
                st.error(f"Error: {e}")


if __name__ == "__main__":
    main()
