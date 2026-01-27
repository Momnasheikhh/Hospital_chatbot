# core/pdf_loader.py
from langchain_community.document_loaders import PyPDFLoader
import os

# PDF path setup
PDF_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "Dow_Hospital_Complete_Information.pdf")

def load_pdf():
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()
    return documents
