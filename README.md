# 🏥 DOW Hospital Chatbot

A modern, intelligent chatbot powered by AI to assist with hospital-related inquiries. Built with LangChain, and a beautiful WhatsApp-inspired Streamlit UI.

## 🌐 Live Demo
You can access the live application here:
**[Hospital Chatbot on Streamlit](https://momnasheikhh-hospital-chatbot-streamlit-app-f4pdup.streamlit.app/)**

## ✨ Features

- 💬 **Real-time Chat** - Instant responses powered by AI
- 🎨 **Modern UI** - WhatsApp-inspired design with smooth animations
- 📷 **Camera Support** - Capture and share photos directly
- 📎 **File Attachment** - Upload files for documentation
- 😊 **Emoji Picker** - 80+ emojis for expression
- 📱 **Responsive Design** - Works seamlessly on all devices
- 🕐 **Message Timestamps** - Track conversation time
- 📅 **Date Separators** - Organized message grouping

## 🛠️ Tech Stack

- **Framework**: Streamlit (Python)
- **AI/ML**: LangChain, RAG (Retrieval-Augmented Generation)
- **Vector DB**: FAISS, OpenAI Embeddings
- **Frontend**: Custom CSS (WhatsApp Style)
- **Icons**: Font Awesome 6.4

## 📋 Requirements

- Python 3.8+
- Virtual Environment
- OpenAI API Key

## 🚀 Quick Start

### 1. Clone & Setup
```bash
git clone https://github.com/yourusername/hospital_chatbot.git
cd hospital_chatbot
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\Activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file with:
```
OPENAI_API_KEY=your_key_here
```

### 5. Run Chatbot
```bash
streamlit run streamlit_app.py
```

Open browser: **http://localhost:8501**

## 📂 Project Structure

```
hospital_chatbot/
├── streamlit_app.py       # Main Streamlit application (Entry Point)
├── app.py                 # Legacy Flask application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── core/
│   ├── chatbot.py       # Chatbot logic
│   ├── embeddings.py    # Vector embeddings (FAISS)
│   ├── pdf_loader.py    # PDF processing logic
│   └── __pycache__/
├── data/
│   └── Dow_Hospital_Complete_Information.pdf  # Hospital documentation
└── web/
    └── style.css        # Stylesheet (for Flask app)
```

## 🎯 How It Works

1. **PDF Loading** - Hospital documentation is processed and indexed
2. **Vector Store** - Documents converted to embeddings using OpenAI
3. **Query Processing** - User questions converted to embeddings
4. **Retrieval** - Most relevant documents retrieved
5. **Response Generation** - LLM generates contextual answers

## 🎨 UI Highlights

- **Header**: Gradient design with hospital branding
- **Messages**: User (blue/purple gradient) & Bot (white)
- **Input Bar**: Minimalist design with quick action buttons
- **Animations**: Smooth slide-in effects for messages
- **Dark Mode Background**: Easy on the eyes

## 📸 Features Demo

| Feature | Description |
|---------|-------------|
| 💬 Chat | Real-time conversation with AI |
| 📷 Camera | Take photos and attach |
| 📎 Files | Upload documents |
| 😊 Emojis | Rich expression support |
| 🕐 Time | Message timestamps |
| 📱 Mobile | Full mobile compatibility |

## 🔐 Security Notes

- API keys stored in `.env` (never commit!)
- `.gitignore` protects sensitive files
- No user data stored permanently
