import os
from pathlib import Path
import httpx
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

AI_PROVIDER = os.getenv("AI_PROVIDER", "mock")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

async def ask_ai(prompt: str) -> str:
    if AI_PROVIDER == "mock":
        # Simple mock reply for testing (reverse + prefix)
        return "AI (mock): " + prompt[::-1]
    if AI_PROVIDER == "groq":
        if not GROQ_API_KEY:
            raise ValueError("AI provider configured as groq but GROQ_API_KEY is empty.")
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",  # Fast and free Groq model
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.7
        }
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                # Parse response depending on provider shape
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise ValueError("Invalid response format from Groq API")
        except httpx.HTTPStatusError as e:
            error_detail = "Unknown error"
            try:
                error_data = e.response.json()
                error_detail = error_data.get("error", {}).get("message", str(e))
            except:
                error_detail = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            raise Exception(f"Groq API error: {error_detail}")
        except httpx.RequestError as e:
            raise Exception(f"Network error connecting to Groq API: {str(e)}")
    raise ValueError(f"AI provider '{AI_PROVIDER}' not configured.")

async def generate_chat_title(messages: list) -> str:
    """Generate a chat title based on conversation context"""
    if AI_PROVIDER == "mock":
        # For mock, just use first user message
        if messages and len(messages) > 0:
            first_user_msg = next((m for m in messages if m.get("role") == "user"), None)
            if first_user_msg:
                text = first_user_msg.get("text", "")
                return text[:50] + "..." if len(text) > 50 else text
        return "New Chat"
    
    if AI_PROVIDER == "groq":
        if not GROQ_API_KEY:
            # Fallback to first message
            if messages and len(messages) > 0:
                first_user_msg = next((m for m in messages if m.get("role") == "user"), None)
                if first_user_msg:
                    text = first_user_msg.get("text", "")
                    return text[:50] + "..." if len(text) > 50 else text
            return "New Chat"
        
        # Build conversation context (first few messages)
        conversation_text = ""
        user_messages = [m for m in messages if m.get("role") == "user"][:3]  # First 3 user messages
        for msg in user_messages:
            conversation_text += msg.get("text", "") + " "
        
        if not conversation_text.strip():
            return "New Chat"
        
        # Generate title using AI
        prompt = f"""Based on this conversation, generate a short, descriptive title (max 6 words, no quotes):
{conversation_text.strip()}

Title:"""
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 20,
            "temperature": 0.3
        }
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                if "choices" in data and len(data["choices"]) > 0:
                    title = data["choices"][0]["message"]["content"].strip()
                    # Clean up title (remove quotes, extra spaces)
                    title = title.replace('"', '').replace("'", "").strip()
                    # Limit to 50 characters
                    if len(title) > 50:
                        title = title[:47] + "..."
                    return title if title else "New Chat"
        except:
            # Fallback to first message if AI fails
            if messages and len(messages) > 0:
                first_user_msg = next((m for m in messages if m.get("role") == "user"), None)
                if first_user_msg:
                    text = first_user_msg.get("text", "")
                    return text[:50] + "..." if len(text) > 50 else text
    
    # Default fallback
    return "New Chat"
