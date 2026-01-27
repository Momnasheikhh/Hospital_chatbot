# core/chatbot.py
from langchain_openai import ChatOpenAI

def create_chatbot(vector_db):
    # LLM setup
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
    retriever = vector_db.as_retriever()
    
    # Create a simple QA chain
    class QAChain:
        def __init__(self, retriever, llm):
            self.retriever = retriever
            self.llm = llm
        
        def invoke(self, inputs):
            query = inputs.get("query", "")
            docs = self.retriever.invoke(query)
            context = "\n".join([doc.page_content for doc in docs])
            
            response = self.llm.invoke(f"Context: {context}\n\nQuestion: {query}")
            return {"result": response.content}
    
    qa_chain = QAChain(retriever, llm)
    return qa_chain
