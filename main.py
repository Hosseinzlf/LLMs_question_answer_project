from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_classic.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA
from dotenv import load_dotenv
import os
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI

google_api_key = os.environ["GOOGLE_API_KEY"]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=google_api_key, temperature=0.5)

vectordb_file_path = "faiss_index"

instructor_embeddings = HuggingFaceInstructEmbeddings()

def create_vector_db():
    # Load CSV with Windows-1252 encoding (detected automatically)
    # Fix for UnicodeDecodeError: Specify the correct encoding

    loader = CSVLoader(
        file_path='codebasics_faqs.csv', 
        source_column='prompt',
        encoding='windows-1252'  # Specify the correct encoding
    )

    # Load the data
    data = loader.load()
    print(f"Successfully loaded {len(data)} documents from CSV!")


    '''
    There are many embedding tools but some of them are not free.
    In this project we use HuggingFaceIntructEmbedding.
    Because it is free but good performing!
    ''' 

    vector_db = FAISS.from_documents(documents=data, embedding = instructor_embeddings)
    vector_db.save_local(vectordb_file_path)


def get_qa_chain():
    vector_db = FAISS.load_local(vectordb_file_path, instructor_embeddings, allow_dangerous_deserialization=True)
    retriever = vector_db.as_retriever()
    prompt_template = """This context is from a CSV file that contains questions and answers. You are a helpful assistant that can answer questions about the context.
    try to answer the question based on the "response" part in the source document without changer it.
    If you didn't find the answer in the documents just say "Appologize, and sayI don't know your answer" and don't try to manipulate or make an answer based on your assumptions

    CONTEXT: {context}

    QUESTION: {question}"""
    
    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type = 'stuff',
            retriever=retriever,
            input_key='query',
            return_source_documents=True,
            chain_type_kwargs=chain_type_kwargs
            )
    return chain

if __name__ == "__main__":
    chain = get_qa_chain()
    print(chain('Do you provide an internship?'))
