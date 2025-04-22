from pymongo import MongoClient
from app.core.config import MONGODB_URL

client = MongoClient(MONGODB_URL)
db = client.ruralhealth

# with this, now have access to collections:
users_collection = db.users
chat_sessions_collection = db.chat_sessions
