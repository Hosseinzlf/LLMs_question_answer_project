from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

google_api_key = os.environ["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=google_api_key, temprature=0)

# Fix for UnicodeDecodeError: Specify the correct encoding
vectordb_file_path = "faiss_index"
# Load CSV with Windows-1252 encoding (detected automatically)
instructor_embeddings = HuggingFaceInstructEmbeddings()

def create_vector_db():
    loader = CSVLoader(
        file_path='codebasics_faqs.csv', 
        source_column='prompt',
        encoding='windows-1252'  # Specify the correct encoding
    )

    # Load the data
    data = loader.load()
    print(f"Successfully loaded {len(data)} documents from CSV!")


    '''
    There are many embedding tools but some of them are not free
    In this project we use HuggingFaceIntructEmbedding
    Because it is free but good performing!
    ''' 

    vector_db = FAISS.from_documents(documents=data, embedding = instructor_embeddings)
    vector_db.save_local(vectordb_file_path)


if __name__ == "__main__":
    create_vector_db()

