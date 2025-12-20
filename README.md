# 🌐 AI Chat App — React + FastAPI + MongoDB  

A full-stack AI chat application with **user authentication**, **multiple chat sessions**, and **persistent chat history**, built using **FastAPI**, **React**, and **MongoDB**.  
The backend generates AI responses using a **mock AI model** or **OpenAI GPT** (optional).

---

## ✨ Features

### 🔐 Authentication  
- User Register & Login (JWT based)  
- Secure password hashing  
- Protected backend routes  

### 💬 Chat System  
- Create, list, and delete chat sessions  
- Persistent message storage in MongoDB  
- Auto-load chat history on refresh  
- AI-generated responses  
- Automatic chat title generation  

### 🎨 Frontend (React + Vite)  
- Modern UI with responsive design  
- Sidebar for chat list  
- Chat bubble UI  
- Auto-scroll to latest message  

### ⚙️ Backend (FastAPI)  
- Async MongoDB using Motor  
- JWT Authentication  
- Modular structure: `main.py`, `auth.py`, `models.py`, `db.py`, `ai_client.py`  
- Clean error handling  

---

## 🛠 Tech Stack

**Frontend:** React, Vite, JavaScript  
**Backend:** FastAPI, Python, Motor  
**Database:** MongoDB Atlas  
**AI Engine:** Mock AI / OpenAI GPT  

---

## 📁 Folder Structure

/frontend → React client
/backend → FastAPI API server


---

## 🚀 Running Locally

### 1️⃣ Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

2️⃣ Frontend Setup

cd frontend
npm install
npm run dev


Frontend URL: http://localhost:5173

Backend URL: http://localhost:8000

🔧 Environment Variables
Backend .env

MONGO_URI=your_mongodb_connection
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
AI_PROVIDER=mock         # or openai
OPENAI_API_KEY=          # only if using OpenAI


Frontend .env
VITE_API_URL=https://your-backend-url.com


📬 API Endpoints
Auth
Method	Endpoint	Description
POST	/register	Register new user
POST	/login	Login & receive JWT
GET	/me	Get authenticated user
Chats
Method	Endpoint	Description
GET	/chats	List all chats
POST	/chats	Create new chat
GET	/chats/{id}	Get chat details
DELETE	/chats/{id}	Remove a chat
Messages
Method	Endpoint	Description
GET	/chats/{id}/messages	Fetch chat history
POST	/message	Send user message & get AI reply
🌍 Deployment
Backend (Render/Railway)

Start command:

uvicorn main:app --host 0.0.0.0 --port $PORT

Frontend (Vercel/Netlify)

Set environment variable in project:

VITE_API_URL=https://your-backend-url.com


Build command:

npm run build



🤖 AI Behavior

Default: Mock AI → reply generated without external API

Optional: Enable OpenAI GPT:

AI_PROVIDER=openai
OPENAI_API_KEY=your_key

👨‍💻 Author

Karthikeya Gaddam
AI/ML & Full-Stack Developer

⭐ Contributions

Pull requests and suggestions are welcome!
If you find a bug, feel free to open an issue.
