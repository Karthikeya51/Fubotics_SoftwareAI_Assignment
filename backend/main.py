# from fastapi import FastAPI, HTTPException, Request, Depends, status
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from datetime import datetime, timedelta

# # Database connection
# from db import users_coll, chats_coll, messages_coll
# from models import MessageIn, UserRegister, UserLogin, UserResponse, Token, ChatCreate, ChatResponse, ChatUpdate
# from ai_client import ask_ai, generate_chat_title
# from auth import (
#     get_password_hash, 
#     verify_password, 
#     create_access_token, 
#     get_current_user,
#     ACCESS_TOKEN_EXPIRE_MINUTES
# )

# app = FastAPI(title="AI Chat with History")

# # Global exception handler
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "detail": str(exc),
#             "type": type(exc).__name__
#         }
#     )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://fubotics-software-ai-assignment-six.vercel.app"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def serialize_message(doc):
#     """Serialize MongoDB message document"""
#     return {
#         "id": str(doc["_id"]),
#         "role": doc["role"],
#         "text": doc["text"],
#         "timestamp": doc["timestamp"].isoformat(),
#         "user_id": str(doc.get("user_id", "")),
#         "chat_id": str(doc.get("chat_id", ""))
#     }

# def serialize_chat(doc, message_count=0):
#     """Serialize MongoDB chat document"""
#     return {
#         "id": str(doc["_id"]),
#         "title": doc.get("title", "New Chat"),
#         "user_id": str(doc["user_id"]),
#         "created_at": doc["created_at"].isoformat(),
#         "updated_at": doc["updated_at"].isoformat(),
#         "message_count": message_count
#     }

# @app.get("/")
# async def root():
#     return {
#         "message": "AI Chat API",
#         "endpoints": {
#             "health": "/health",
#             "register": "/register (POST)",
#             "login": "/login (POST)",
#             "me": "/me (GET, requires auth)",
#             "history": "/history (GET, requires auth)",
#             "message": "/message (POST, requires auth)",
#             "docs": "/docs"
#         }
#     }

# @app.get("/health")
# async def health():
#     try:
#         # Test database connection
#         await messages_coll.find_one()
#         await users_coll.find_one()
#         await chats_coll.find_one()
#         return {"status": "ok", "database": "connected"}
#     except Exception as e:
#         return {"status": "ok", "database": "disconnected", "error": str(e)}

# @app.post("/register", response_model=UserResponse)
# async def register(user_data: UserRegister):
#     """Register a new user"""
#     try:
#         # Check if user already exists
#         existing_user = await users_coll.find_one({"$or": [{"username": user_data.username}, {"email": user_data.email}]})
#         if existing_user:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Username or email already registered"
#             )
        
#         # Create new user
#         user_doc = {
#             "username": user_data.username,
#             "email": user_data.email,
#             "hashed_password": get_password_hash(user_data.password),
#             "created_at": datetime.utcnow()
#         }
#         result = await users_coll.insert_one(user_doc)
        
#         return UserResponse(
#             id=str(result.inserted_id),
#             username=user_data.username,
#             email=user_data.email
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

# @app.post("/login", response_model=Token)
# async def login(user_data: UserLogin):
#     """Login user and return JWT token"""
#     try:
#         # Find user
#         user = await users_coll.find_one({"username": user_data.username})
#         if not user:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password"
#             )
        
#         # Verify password
#         if not verify_password(user_data.password, user["hashed_password"]):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Incorrect username or password"
#             )
        
#         # Create access token
#         access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         access_token = create_access_token(
#             data={"sub": user["username"]},
#             expires_delta=access_token_expires
#         )
        
#         return Token(access_token=access_token, token_type="bearer")
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

# @app.get("/me", response_model=UserResponse)
# async def get_current_user_info(username: str = Depends(get_current_user)):
#     """Get current user information"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return UserResponse(
#             id=str(user["_id"]),
#             username=user["username"],
#             email=user["email"]
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# @app.post("/chats", response_model=ChatResponse)
# async def create_chat(chat_data: ChatCreate, username: str = Depends(get_current_user)):
#     """Create a new chat"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         now = datetime.utcnow()
#         chat_doc = {
#             "title": chat_data.title or "New Chat",
#             "user_id": user_id,
#             "created_at": now,
#             "updated_at": now
#         }
#         result = await chats_coll.insert_one(chat_doc)
        
#         return ChatResponse(
#             id=str(result.inserted_id),
#             title=chat_doc["title"],
#             user_id=user_id,
#             created_at=now,
#             updated_at=now,
#             message_count=0
#         )
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")

# @app.get("/chats", response_model=list[ChatResponse])
# async def list_chats(username: str = Depends(get_current_user)):
#     """List all chats for current user"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         # Fetch all chats for user
#         cursor = chats_coll.find({"user_id": user_id}).sort("updated_at", -1)
#         chats = await cursor.to_list(length=100)
        
#         # Get message count for each chat
#         result = []
#         for chat in chats:
#             chat_id = str(chat["_id"])
#             message_count = await messages_coll.count_documents({"chat_id": chat_id})
#             result.append(serialize_chat(chat, message_count))
        
#         return result
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

# @app.get("/chats/{chat_id}", response_model=ChatResponse)
# async def get_chat(chat_id: str, username: str = Depends(get_current_user)):
#     """Get a specific chat"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         from bson import ObjectId
#         chat = await chats_coll.find_one({"_id": ObjectId(chat_id), "user_id": user_id})
#         if not chat:
#             raise HTTPException(status_code=404, detail="Chat not found")
        
#         message_count = await messages_coll.count_documents({"chat_id": chat_id})
#         return serialize_chat(chat, message_count)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching chat: {str(e)}")

# @app.put("/chats/{chat_id}", response_model=ChatResponse)
# async def update_chat(chat_id: str, chat_data: ChatUpdate, username: str = Depends(get_current_user)):
#     """Update chat title"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         from bson import ObjectId
#         result = await chats_coll.update_one(
#             {"_id": ObjectId(chat_id), "user_id": user_id},
#             {"$set": {"title": chat_data.title, "updated_at": datetime.utcnow()}}
#         )
        
#         if result.matched_count == 0:
#             raise HTTPException(status_code=404, detail="Chat not found")
        
#         chat = await chats_coll.find_one({"_id": ObjectId(chat_id)})
#         message_count = await messages_coll.count_documents({"chat_id": chat_id})
#         return serialize_chat(chat, message_count)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error updating chat: {str(e)}")

# @app.delete("/chats/{chat_id}")
# async def delete_chat(chat_id: str, username: str = Depends(get_current_user)):
#     """Delete a chat and all its messages"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         from bson import ObjectId
#         result = await chats_coll.delete_one({"_id": ObjectId(chat_id), "user_id": user_id})
#         if result.deleted_count == 0:
#             raise HTTPException(status_code=404, detail="Chat not found")
        
#         # Delete all messages in this chat
#         await messages_coll.delete_many({"chat_id": chat_id})
        
#         return {"message": "Chat deleted successfully"}
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

# @app.get("/chats/{chat_id}/messages")
# async def get_chat_messages(chat_id: str, username: str = Depends(get_current_user)):
#     """Get messages for a specific chat"""
#     try:
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         from bson import ObjectId
#         # Verify chat belongs to user
#         chat = await chats_coll.find_one({"_id": ObjectId(chat_id), "user_id": user_id})
#         if not chat:
#             raise HTTPException(status_code=404, detail="Chat not found")
        
#         # Fetch messages for this chat
#         cursor = messages_coll.find({"chat_id": chat_id}).sort("timestamp", 1)
#         docs = await cursor.to_list(length=1000)
#         return [serialize_message(d) for d in docs]
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

# @app.post("/message")
# async def post_message(msg: MessageIn, username: str = Depends(get_current_user)):
#     """Send a message and get AI response (requires authentication)"""
#     try:
#         # Get user ID
#         user = await users_coll.find_one({"username": username})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         user_id = str(user["_id"])
        
#         # Get or create chat
#         from bson import ObjectId
#         if msg.chat_id:
#             # Verify chat belongs to user
#             chat = await chats_coll.find_one({"_id": ObjectId(msg.chat_id), "user_id": user_id})
#             if not chat:
#                 raise HTTPException(status_code=404, detail="Chat not found")
#             chat_id = msg.chat_id
#         else:
#             # Create new chat - title will be generated after first AI response
#             now = datetime.utcnow()
#             chat_doc = {
#                 "title": "New Chat",
#                 "user_id": user_id,
#                 "created_at": now,
#                 "updated_at": now
#             }
#             chat_result = await chats_coll.insert_one(chat_doc)
#             chat_id = str(chat_result.inserted_id)
        
#         # Save user message to database
#         user_doc = {
#             "role": "user",
#             "text": msg.text,
#             "timestamp": datetime.utcnow(),
#             "user_id": user_id,
#             "chat_id": chat_id
#         }
#         inserted_user = await messages_coll.insert_one(user_doc)

#         # Get AI response
#         try:
#             ai_text = await ask_ai(msg.text)
#         except Exception as e:
#             # Remove user message from database if AI fails
#             await messages_coll.delete_one({"_id": inserted_user.inserted_id})
#             raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

#         # Save AI message to database
#         ai_doc = {
#             "role": "ai",
#             "text": ai_text,
#             "timestamp": datetime.utcnow(),
#             "user_id": user_id,
#             "chat_id": chat_id
#         }
#         inserted_ai = await messages_coll.insert_one(ai_doc)

#         # Generate/update chat title based on conversation context
#         try:
#             # Get all messages in this chat
#             cursor = messages_coll.find({"chat_id": chat_id}).sort("timestamp", 1)
#             all_messages = await cursor.to_list(length=10)  # Get first 10 messages for context
            
#             # Generate title from conversation context
#             title = await generate_chat_title(all_messages)
            
#             # Update chat title and updated_at
#             await chats_coll.update_one(
#                 {"_id": ObjectId(chat_id)},
#                 {"$set": {"title": title, "updated_at": datetime.utcnow()}}
#             )
#         except Exception as e:
#             # If title generation fails, just update timestamp
#             await chats_coll.update_one(
#                 {"_id": ObjectId(chat_id)},
#                 {"$set": {"updated_at": datetime.utcnow()}}
#             )

#         # Return the saved user and ai messages
#         return {
#             "chat_id": chat_id,
#             "user": {
#                 "id": str(inserted_user.inserted_id),
#                 "role": "user",
#                 "text": user_doc["text"],
#                 "timestamp": user_doc["timestamp"].isoformat()
#             },
#             "ai": {
#                 "id": str(inserted_ai.inserted_id),
#                 "role": "ai",
#                 "text": ai_doc["text"],
#                 "timestamp": ai_doc["timestamp"].isoformat()
#             }
#         }
#     except HTTPException:
#         # Re-raise HTTP exceptions as-is
#         raise
#     except Exception as e:
#         # Catch any other unexpected errors
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# backend/main.py
from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Any

# Database connection
from db import users_coll, chats_coll, messages_coll
from models import MessageIn, UserRegister, UserLogin, UserResponse, Token, ChatCreate, ChatResponse, ChatUpdate
from ai_client import ask_ai, generate_chat_title
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(title="AI Chat with History")

# Global exception handler (helpful during debugging)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serialization helpers ---
def serialize_message(doc: dict) -> dict:
    """Serialize MongoDB message document to JSON-friendly dict."""
    return {
        "id": str(doc.get("_id")),
        "role": doc.get("role"),
        "text": doc.get("text"),
        "timestamp": doc.get("timestamp").isoformat() if doc.get("timestamp") else None,
        "user_id": str(doc.get("user_id", "")),
        "chat_id": str(doc.get("chat_id", ""))
    }

def serialize_chat(doc: dict, message_count: int = 0) -> dict:
    """Serialize MongoDB chat document to JSON-friendly dict."""
    return {
        "id": str(doc.get("_id")),
        "title": doc.get("title", "New Chat"),
        "user_id": str(doc.get("user_id", "")),
        "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
        "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None,
        "message_count": int(message_count)
    }

# --- Root & health ---
@app.get("/")
async def root():
    return {
        "message": "AI Chat API",
        "endpoints": {
            "health": "/health",
            "register": "/register (POST)",
            "login": "/login (POST)",
            "me": "/me (GET, requires auth)",
            "chats": "/chats (GET/POST, requires auth)",
            "chat messages": "/chats/{chat_id}/messages (GET, requires auth)",
            "message": "/message (POST, requires auth)",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    try:
        # Test database connection (simple probe)
        await messages_coll.find_one()
        await users_coll.find_one()
        await chats_coll.find_one()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "ok", "database": "disconnected", "error": str(e)}

# --- Auth: Register & Login ---
@app.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserRegister):
    """Register a new user"""
    try:
        existing_user = await users_coll.find_one(
            {"$or": [{"username": user_data.username}, {"email": user_data.email}]}
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )

        user_doc = {
            "username": user_data.username,
            "email": user_data.email,
            "hashed_password": get_password_hash(user_data.password),
            "created_at": datetime.utcnow()
        }
        result = await users_coll.insert_one(user_doc)

        return UserResponse(
            id=str(result.inserted_id),
            username=user_data.username,
            email=user_data.email
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration error: {str(e)}")

@app.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Login user and return JWT token"""
    try:
        user = await users_coll.find_one({"username": user_data.username})
        if not user or not verify_password(user_data.password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # create token with subject as user id (more robust than username)
        access_token = create_access_token(
            data={"sub": str(user["_id"])},
            expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

# --- Helper to normalize current_user dependency output ---
async def resolve_current_user_info(current_user_dep: Any) -> dict:
    """
    Accepts either:
      - a dict returned by get_current_user (containing at least 'id'/'username'), OR
      - a username string (older variants).
    Returns a user dict from DB with fields (_id, username, email).
    """
    # If get_current_user returned dict with id/username, try to use it
    if isinstance(current_user_dep, dict):
        # If it already contains full info, try to use it directly
        if "id" in current_user_dep and "username" in current_user_dep:
            # Optionally fetch fresh user record to get DB _id and email
            u = await users_coll.find_one({"_id": current_user_dep.get("id")}) \
                if isinstance(current_user_dep.get("id"), str) else None
            if u:
                return u
            # fallback: try by username
            u = await users_coll.find_one({"username": current_user_dep.get("username")})
            if u:
                return u
        # fallback: try if dict contains username only
        if "username" in current_user_dep:
            u = await users_coll.find_one({"username": current_user_dep["username"]})
            if u:
                return u

    # If it's a plain string, treat as user id or username
    if isinstance(current_user_dep, str):
        # try by id first
        from bson import ObjectId
        try:
            u = await users_coll.find_one({"_id": ObjectId(current_user_dep)})
            if u:
                return u
        except Exception:
            pass
        # try by username
        u = await users_coll.find_one({"username": current_user_dep})
        if u:
            return u

    # Not resolvable
    raise HTTPException(status_code=401, detail="Invalid authentication principal")

# --- Me endpoint ---
@app.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information"""
    try:
        user = await resolve_current_user_info(current_user)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse(id=str(user["_id"]), username=user["username"], email=user["email"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

# --- Chat CRUD ---
@app.post("/chats", response_model=ChatResponse, status_code=201)
async def create_chat(chat_data: ChatCreate, current_user = Depends(get_current_user)):
    """Create a new chat"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        now = datetime.utcnow()
        chat_doc = {
            "title": chat_data.title or "New Chat",
            "user_id": user_id,
            "created_at": now,
            "updated_at": now
        }
        result = await chats_coll.insert_one(chat_doc)

        return ChatResponse(
            id=str(result.inserted_id),
            title=chat_doc["title"],
            user_id=user_id,
            created_at=now,
            updated_at=now,
            message_count=0
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating chat: {str(e)}")

@app.get("/chats", response_model=list[ChatResponse])
async def list_chats(current_user = Depends(get_current_user)):
    """List all chats for current user"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        cursor = chats_coll.find({"user_id": user_id}).sort("updated_at", -1)
        chats = await cursor.to_list(length=100)

        result = []
        for chat in chats:
            chat_id_str = str(chat["_id"])
            message_count = await messages_coll.count_documents({"chat_id": chat_id_str})
            result.append(serialize_chat(chat, message_count))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chats: {str(e)}")

@app.get("/chats/{chat_id}", response_model=ChatResponse)
async def get_chat(chat_id: str, current_user = Depends(get_current_user)):
    """Get a specific chat"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        from bson import ObjectId
        chat = await chats_coll.find_one({"_id": ObjectId(chat_id), "user_id": user_id})
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        message_count = await messages_coll.count_documents({"chat_id": chat_id})
        return serialize_chat(chat, message_count)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat: {str(e)}")

@app.put("/chats/{chat_id}", response_model=ChatResponse)
async def update_chat(chat_id: str, chat_data: ChatUpdate, current_user = Depends(get_current_user)):
    """Update chat title"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        from bson import ObjectId
        result = await chats_coll.update_one(
            {"_id": ObjectId(chat_id), "user_id": user_id},
            {"$set": {"title": chat_data.title, "updated_at": datetime.utcnow()}}
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Chat not found")

        chat = await chats_coll.find_one({"_id": ObjectId(chat_id)})
        message_count = await messages_coll.count_documents({"chat_id": chat_id})
        return serialize_chat(chat, message_count)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating chat: {str(e)}")

@app.delete("/chats/{chat_id}")
async def delete_chat(chat_id: str, current_user = Depends(get_current_user)):
    """Delete a chat and all its messages"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        from bson import ObjectId
        result = await chats_coll.delete_one({"_id": ObjectId(chat_id), "user_id": user_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Delete all messages (we store chat_id as string)
        await messages_coll.delete_many({"chat_id": chat_id})

        return {"message": "Chat deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chat: {str(e)}")

# --- Messages ---
@app.get("/chats/{chat_id}/messages")
async def get_chat_messages(chat_id: str, current_user = Depends(get_current_user)):
    """Get messages for a specific chat"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])

        from bson import ObjectId
        # Verify chat belongs to user
        chat = await chats_coll.find_one({"_id": ObjectId(chat_id), "user_id": user_id})
        if not chat:
            raise HTTPException(status_code=404, detail="Chat not found")

        # Fetch messages for this chat (chat_id is stored as string)
        cursor = messages_coll.find({"chat_id": chat_id}).sort("timestamp", 1)
        docs = await cursor.to_list(length=1000)
        return [serialize_message(d) for d in docs]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")

@app.post("/message")
async def post_message(msg: MessageIn, current_user = Depends(get_current_user)):
    """Send a message and get AI response (requires authentication)"""
    try:
        user = await resolve_current_user_info(current_user)
        user_id = str(user["_id"])
        username = user.get("username")

        # Get or create chat
        from bson import ObjectId
        if msg.chat_id:
            # Verify chat belongs to user
            chat = await chats_coll.find_one({"_id": ObjectId(msg.chat_id), "user_id": user_id})
            if not chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            chat_id = msg.chat_id
        else:
            # Create new chat - title will be generated after first AI response
            now = datetime.utcnow()
            chat_doc = {
                "title": "New Chat",
                "user_id": user_id,
                "created_at": now,
                "updated_at": now
            }
            chat_result = await chats_coll.insert_one(chat_doc)
            chat_id = str(chat_result.inserted_id)

        # Save user message to database (store chat_id as string)
        user_doc = {
            "role": "user",
            "text": msg.text,
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "chat_id": chat_id
        }
        inserted_user = await messages_coll.insert_one(user_doc)

        # Get AI response
        try:
            ai_text = await ask_ai(msg.text)
        except Exception as e:
            # Remove user message from database if AI fails
            await messages_coll.delete_one({"_id": inserted_user.inserted_id})
            raise HTTPException(status_code=500, detail=f"AI error: {str(e)}")

        # Save AI message to database
        ai_doc = {
            "role": "ai",
            "text": ai_text,
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "chat_id": chat_id
        }
        inserted_ai = await messages_coll.insert_one(ai_doc)

        # Generate/update chat title based on conversation context (best-effort)
        try:
            cursor = messages_coll.find({"chat_id": chat_id}).sort("timestamp", 1)
            all_messages = await cursor.to_list(length=10)
            title = await generate_chat_title(all_messages)
            # update chat title (if chat exists)
            await chats_coll.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"title": title, "updated_at": datetime.utcnow()}}
            )
        except Exception:
            # If any part fails, still continue — update timestamp to mark activity
            await chats_coll.update_one(
                {"_id": ObjectId(chat_id)},
                {"$set": {"updated_at": datetime.utcnow()}}
            )

        # Return the saved user and ai messages
        return {
            "chat_id": chat_id,
            "user": {
                "id": str(inserted_user.inserted_id),
                "role": "user",
                "text": user_doc["text"],
                "timestamp": user_doc["timestamp"].isoformat()
            },
            "ai": {
                "id": str(inserted_ai.inserted_id),
                "role": "ai",
                "text": ai_doc["text"],
                "timestamp": ai_doc["timestamp"].isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
