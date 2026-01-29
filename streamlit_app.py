import streamlit as st
import os
from dotenv import load_dotenv
from core.pdf_loader import load_pdf
from core.embeddings import create_vector_store
from core.chatbot import create_chatbot

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Dow Hospital Chatbot",
    page_icon="🏥",
    layout="centered"
)

# Custom CSS for WhatsApp-style premium look
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: #0b141a;
        color: #e9edef;
    }
    
    /* Header Styling */
    .stHeader {
        background: #202c33;
        padding: 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Chat Container Spacing */
    .block-container {
        padding-top: 2rem !important;
        max-width: 800px !important;
    }

    /* WhatsApp Style Bubbles */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 5px !important;
    }

    /* Assistant Bubble (Left) */
    [data-testid="stChatMessageAssistant"] .stChatMessageContent {
        background-color: #202c33 !important;
        border-radius: 0 15px 15px 15px !important;
        padding: 12px 16px !important;
        max-width: 80% !important;
        color: #e9edef !important;
        margin-right: auto !important;
    }

    /* User Bubble (Right) */
    [data-testid="stChatMessageUser"] .stChatMessageContent {
        background-color: #005c4b !important;
        border-radius: 15px 0 15px 15px !important;
        padding: 12px 16px !important;
        max-width: 80% !important;
        color: #e9edef !important;
        margin-left: auto !important;
        text-align: left !important;
    }
    
    /* Avatar hiding for cleaner look */
    [data-testid="stChatMessageAvatarAssistant"], [data-testid="stChatMessageAvatarUser"] {
        display: none !important;
    }

    /* Chat Input Styling */
    .stChatInputContainer {
        padding-bottom: 30px !important;
        background-color: #0b141a !important;
    }
    
    .stChatInput textarea {
        background-color: #2a3942 !important;
        color: #e9edef !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 12px 20px !important;
    }

    /* Hide the sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* Spinner Styling */
    .stSpinner {
        text-align: center;
        color: #00a884;
    }
    
    hr {
        border-color: rgba(255,255,255,0.1) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize chatbot and vector store as cached resources
@st.cache_resource
def initialize_system():
    try:
        # Silent initialization
        docs = load_pdf()
        vector_db = create_vector_store(docs)
        return create_chatbot(vector_db)
    except Exception as e:
        return None

# App header
st.title("🏥 Dow Hospital Assistant")
st.markdown("<p style='opacity: 0.7; font-size: 0.9em;'>AI-powered medical inquiry assistant</p>", unsafe_allow_html=True)
st.markdown("---")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your Dow Hospital Assistant. How can I help you today?"}
    ]

# Show messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System initialization (Quiet load)
if "chatbot_ready" not in st.session_state:
    with st.spinner("Preparing system..."):
        chatbot = initialize_system()
        if chatbot:
            st.session_state.chatbot_ready = chatbot
            st.rerun()
else:
    chatbot = st.session_state.chatbot_ready

if chatbot:
    # Chat input
    if prompt := st.chat_input("Type your question here..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        try:
            with st.spinner("Searching records..."):
                result = chatbot.invoke({"query": prompt})
                response = result.get("result", "I couldn't find specific information on that.")
            
            with st.chat_message("assistant"):
                st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Something went wrong. Please try again.")
else:
    st.info("System is being configured. Please wait a moment...")
