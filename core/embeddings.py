# core/embeddings.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(documents):
    # OpenAI embeddings ke sath FAISS vector store
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(documents, embeddings)
    return vector_db
