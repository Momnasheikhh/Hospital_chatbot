#!/usr/bin/env python
from flask import Flask, render_template_string, request, jsonify
from core.pdf_loader import load_pdf
from core.embeddings import create_vector_store
from core.chatbot import create_chatbot
import os
from dotenv import load_dotenv

load_dotenv()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dow Hospital Chatbot</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html, body { height: 100%; width: 100%; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            width: 100%;
            max-width: 500px;
            height: 90vh;
            background: white;
            border-radius: 30px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
            color: white;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
        }
        
        .header-avatar {
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }
        
        .header-info h1 {
            font-size: 18px;
            margin: 0;
            font-weight: 600;
        }
        
        .header-info p {
            font-size: 12px;
            margin: 2px 0 0 0;
            opacity: 0.9;
        }
        
        .chat-box {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
            background: #f8fafc;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        
        .message-group {
            display: flex;
            width: 100%;
            margin-bottom: 12px;
        }
        
        .message-group.user {
            justify-content: flex-end;
        }
        
        .message-group.bot {
            justify-content: flex-start;
        }
        
        .message-wrapper {
            display: flex;
            align-items: flex-end;
            gap: 6px;
            max-width: 75%;
        }
        
        .message-group.user .message-wrapper {
            flex-direction: row-reverse;
            justify-content: flex-end;
        }
        
        .bot-msg {
            background: white;
            color: #333;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            word-wrap: break-word;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            font-size: 15px;
            line-height: 1.4;
        }
        
        .user-msg {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            word-wrap: break-word;
            font-size: 15px;
            line-height: 1.4;
        }
        
        .msg-time {
            font-size: 12px;
            white-space: nowrap;
            padding: 0 4px;
            margin-bottom: 2px;
        }
        
        .user-msg .msg-time {
            color: rgba(255, 255, 255, 0.8);
        }
        
        .bot-msg .msg-time {
            color: #999;
        }
        
        .date-separator {
            text-align: center;
            margin: 16px 0;
            font-size: 12px;
            color: #999;
            font-weight: 500;
        }
        
        .input-box {
            display: flex;
            gap: 8px;
            padding: 12px 16px;
            background: white;
            border-top: 1px solid #eee;
            align-items: flex-end;
        }
        
        .input-icons {
            display: flex;
            gap: 6px;
        }
        
        .input-icon-btn {
            background: none;
            border: none;
            color: #3b82f6;
            font-size: 20px;
            cursor: pointer;
            padding: 6px;
            transition: all 0.2s ease;
        }
        
        .input-icon-btn:hover {
            color: #8b5cf6;
            transform: scale(1.1);
        }
        
        .input-wrapper {
            flex: 1;
            display: flex;
            align-items: center;
            background: #f0f0f0;
            border-radius: 25px;
            padding: 10px 16px;
        }
        
        input#msg {
            flex: 1;
            border: none;
            background: transparent;
            font-size: 15px;
            font-family: inherit;
            outline: none;
            color: #333;
        }
        
        input#msg::placeholder {
            color: #999;
        }
        
        #send-btn {
            width: 40px;
            height: 40px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        #send-btn:hover {
            transform: scale(1.1);
        }
        
        .emoji-picker {
            display: none;
            position: absolute;
            bottom: 80px;
            right: 60px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 12px;
            z-index: 1000;
            grid-template-columns: repeat(6, 1fr);
            gap: 8px;
            width: 280px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .emoji-picker.show {
            display: grid;
        }
        
        .emoji-item {
            font-size: 28px;
            cursor: pointer;
            padding: 8px;
            border-radius: 8px;
            text-align: center;
            user-select: none;
        }
        
        .emoji-item:hover {
            background: #f0f0f0;
            transform: scale(1.2);
        }
        
        .camera-modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.9);
            z-index: 2000;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .camera-modal.show {
            display: flex;
        }
        
        .camera-container {
            position: relative;
            width: 100%;
            max-width: 500px;
            height: 600px;
            background: #000;
            border-radius: 15px;
            overflow: hidden;
        }
        
        #cameraVideo {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        #cameraCanvas {
            display: none;
        }
        
        .camera-controls {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            justify-content: center;
        }
        
        .camera-btn {
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            cursor: pointer;
            font-weight: 600;
        }
        
        .camera-btn.capture {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
        }
        
        .camera-btn.close {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px 20px;
        }
        
        #fileInput {
            display: none;
        }
        
        .file-upload-indicator {
            position: fixed;
            bottom: 100px;
            right: 20px;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 8px;
            display: none;
            z-index: 999;
        }
        
        .file-upload-indicator.show {
            display: block;
        }
        
        @media (max-width: 600px) {
            .container {
                height: 100vh;
                border-radius: 0;
                max-width: 100%;
            }
            .bot-msg, .user-msg {
                max-width: 85%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-avatar">🏥</div>
            <div class="header-info">
                <h1>DOW Hospital</h1>
                <p>🟢 Online</p>
            </div>
        </div>
        
        <div class="chat-box">
            <div style="margin: auto;">
                <div style="text-align: center; color: #999; font-size: 14px;">
                    <div style="font-size: 40px; margin-bottom: 10px;">🏥</div>
                    <div style="font-weight: 600; font-size: 16px; color: #333;">DOW Hospital Assistant</div>
                    <div style="font-size: 13px; color: #999; margin-top: 8px;">Always here to help</div>
                </div>
            </div>
        </div>
        
        <div class="input-box">
            <div class="input-icons">
                <button class="input-icon-btn" id="attachBtn"><i class="fas fa-paperclip"></i></button>
                <button class="input-icon-btn" id="cameraBtn"><i class="fas fa-camera"></i></button>
            </div>
            <div class="input-wrapper">
                <input id="msg" placeholder="Type your question..." />
                <button class="input-icon-btn" id="emojiBtn"><i class="fas fa-smile"></i></button>
            </div>
            <button id="send-btn" onclick="send()"><i class="fas fa-paper-plane"></i></button>
            <div class="emoji-picker" id="emojiPicker"></div>
        </div>
        
        <input type="file" id="fileInput" />
        
        <div class="camera-modal" id="cameraModal">
            <div class="camera-container">
                <video id="cameraVideo" autoplay playsinline></video>
                <canvas id="cameraCanvas"></canvas>
            </div>
            <div class="camera-controls">
                <button class="camera-btn close" id="closeCameraBtn">Close</button>
                <button class="camera-btn capture" id="captureBtn">📸</button>
            </div>
        </div>
        
        <div class="file-upload-indicator" id="uploadIndicator"></div>
    </div>

    <script>
        const msgInput = document.getElementById("msg");
        const chatBox = document.querySelector(".chat-box");
        const emojiBtn = document.getElementById("emojiBtn");
        const emojiPicker = document.getElementById("emojiPicker");
        const cameraBtn = document.getElementById("cameraBtn");
        const attachBtn = document.getElementById("attachBtn");
        const fileInput = document.getElementById("fileInput");
        const cameraModal = document.getElementById("cameraModal");
        const cameraVideo = document.getElementById("cameraVideo");
        const cameraCanvas = document.getElementById("cameraCanvas");
        const captureBtn = document.getElementById("captureBtn");
        const closeCameraBtn = document.getElementById("closeCameraBtn");
        const uploadIndicator = document.getElementById("uploadIndicator");
        
        let lastMessageDate = null;
        const emojis = ['😀', '😂', '😍', '🥰', '😢', '😭', '😱', '😎', '🤔', '👍', '❤️', '🎉', '🙏', '✨', '💯', '😃', '😄', '😁', '😆', '😅', '🤣', '😉', '😊', '😇', '🤩', '😘', '😗', '😚', '😙', '🥲', '😋', '😛', '😜', '🤪', '😌', '😔', '😑', '😐', '😏', '😒', '🙁', '😬', '😮', '😯', '😲', '😳', '🥺', '😦', '😧', '😨', '😰', '😥', '😞', '😓', '😩', '😫', '🥱', '😤', '😡', '😠', '💀', '💩', '🤡', '👹', '👻', '👽', '👾', '🤖', '💋', '💌', '💘', '💝', '💖', '💗', '💓', '💞', '💕'];
        
        function initEmojis() {
            emojis.forEach(emoji => {
                const item = document.createElement('div');
                item.className = 'emoji-item';
                item.textContent = emoji;
                item.addEventListener('click', () => {
                    msgInput.value += emoji;
                    msgInput.focus();
                    emojiPicker.classList.remove('show');
                });
                emojiPicker.appendChild(item);
            });
        }
        
        emojiBtn.addEventListener('click', (e) => {
            e.preventDefault();
            emojiPicker.classList.toggle('show');
        });
        
        document.addEventListener('click', (e) => {
            if (!emojiPicker.contains(e.target) && e.target !== emojiBtn && !emojiBtn.contains(e.target)) {
                emojiPicker.classList.remove('show');
            }
        });
        
        cameraBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } });
                cameraVideo.srcObject = stream;
                cameraModal.classList.add('show');
            } catch (err) {
                alert('Camera access denied.');
            }
        });
        
        closeCameraBtn.addEventListener('click', () => {
            cameraVideo.srcObject.getTracks().forEach(track => track.stop());
            cameraModal.classList.remove('show');
        });
        
        captureBtn.addEventListener('click', () => {
            const ctx = cameraCanvas.getContext('2d');
            cameraCanvas.width = cameraVideo.videoWidth;
            cameraCanvas.height = cameraVideo.videoHeight;
            ctx.drawImage(cameraVideo, 0, 0);
            addMessage('📷 Photo: ' + new Date().toLocaleTimeString(), true);
            cameraVideo.srcObject.getTracks().forEach(track => track.stop());
            cameraModal.classList.remove('show');
        });
        
        attachBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fileInput.click();
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                const file = e.target.files[0];
                uploadIndicator.textContent = '✅ ' + file.name;
                uploadIndicator.classList.add('show');
                addMessage('📎 ' + file.name, true);
                setTimeout(() => uploadIndicator.classList.remove('show'), 3000);
            }
        });
        
        function getTime() {
            const now = new Date();
            return now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        }
        
        function addMessage(text, isUser) {
            const now = new Date();
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (lastMessageDate !== now.toDateString()) {
                let dateStr = 'Today';
                if (now.toDateString() === yesterday.toDateString()) dateStr = 'Yesterday';
                else if (now.getFullYear() !== today.getFullYear()) dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                else dateStr = now.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                
                const separator = document.createElement("div");
                separator.className = "date-separator";
                separator.textContent = dateStr;
                chatBox.appendChild(separator);
                lastMessageDate = now.toDateString();
            }
            
            const messageGroup = document.createElement("div");
            messageGroup.className = "message-group " + (isUser ? "user" : "bot");
            
            const wrapper = document.createElement("div");
            wrapper.className = "message-wrapper";
            
            const msgDiv = document.createElement("div");
            msgDiv.className = isUser ? "user-msg" : "bot-msg";
            msgDiv.textContent = text;
            
            const timeDiv = document.createElement("div");
            timeDiv.className = "msg-time";
            timeDiv.textContent = getTime();
            
            wrapper.appendChild(msgDiv);
            wrapper.appendChild(timeDiv);
            messageGroup.appendChild(wrapper);
            chatBox.appendChild(messageGroup);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function send(){
            let msg = msgInput.value.trim();
            if(!msg) return;
            addMessage(msg, true);
            msgInput.value = "";
            
            fetch("/chat", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body:JSON.stringify({message:msg})
            })
            .then(res => res.json())
            .then(data => addMessage(data.reply, false))
            .catch(err => addMessage("Error: " + err, false));
        }
        
        msgInput.addEventListener("keypress", (e) => {
            if(e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
            }
        });
        
        initEmojis();
    </script>
</body>
</html>
'''

app = Flask(__name__)

print("Loading PDF...")
try:
    docs = load_pdf()
    print(f"PDF loaded: {len(docs)} pages")
    vector_db = create_vector_store(docs)
    print("Vector store created")
    chatbot = create_chatbot(vector_db)
    print("Chatbot ready!")
except Exception as e:
    print(f"ERROR: {e}")
    chatbot = None

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        if not chatbot:
            return jsonify({"reply": "Error: Chatbot not initialized"})
        
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"reply": "Error: No message"})
        
        user_msg = data["message"].strip()
        if not user_msg:
            return jsonify({"reply": "Error: Empty message"})
        
        print(f"User: {user_msg}")
        result = chatbot.invoke({"query": user_msg})
        answer = result.get("result", "I don't have an answer").strip()
        
        print(f"Bot: {answer}")
        return jsonify({"reply": answer})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    print("Starting: http://127.0.0.1:5000")
    app.run(debug=True, host="127.0.0.1", port=5000)
