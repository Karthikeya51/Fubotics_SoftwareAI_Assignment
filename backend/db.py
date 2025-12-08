import os
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env from backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create MongoDB client with connection timeout
client = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000  # 5 second timeout
)
db = client["chatdb"]

# Collections
users_coll = db["users"]
chats_coll = db["chats"]
messages_coll = db["messages"]
