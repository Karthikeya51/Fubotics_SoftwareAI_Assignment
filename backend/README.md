Backend (FastAPI) for AI Chat App
--------------------------------

Setup (local):

1. Create virtualenv: python -m venv .venv
2. Activate:
   - Windows: .venv\Scripts\activate
   - macOS/Linux: source .venv/bin/activate
3. Install: pip install -r requirements.txt
4. Copy .env.example to .env and edit MONGO_URI (and GROQ_API_KEY if using Groq)
5. Run: uvicorn main:app --reload --port 8000

Endpoints:
- GET /health
- GET /history
- POST /message  { "text": "hello" }

Notes:
- Default AI_PROVIDER is 'mock' which returns a reversed-text reply.
- For production, set AI_PROVIDER=groq and provide GROQ_API_KEY.
- Get your Groq API key from: https://console.groq.com/
