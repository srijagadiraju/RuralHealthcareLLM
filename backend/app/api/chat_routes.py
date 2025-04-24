from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.services.db import chat_sessions_collection

router = APIRouter()

# ===== Schemas =====


class Message(BaseModel):
    sender: str
    text: str
    sources: Optional[List[str]] = []  # <-- Added this


class ChatSessionCreate(BaseModel):
    user_id: str
    title: str


class MessageAppend(BaseModel):
    sender: str
    text: str
    sources: Optional[List[str]] = []  # <-- Added this


# ===== Routes =====

# Create a new chat session
@router.post("/chats/new")
def create_chat_session(chat: ChatSessionCreate):
    if not chat.user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    new_chat = {
        "user_id": chat.user_id,
        "title": chat.title,
        "created_at": datetime.utcnow(),
        "last_interacted_at": datetime.utcnow(),
        "messages": []
    }
    result = chat_sessions_collection.insert_one(new_chat)
    return {"chat_id": str(result.inserted_id), "message": "Chat session created"}


# Append a new message to an existing chat
@router.post("/chats/{chat_id}/message")
def append_message(chat_id: str, msg: MessageAppend):
    chat = chat_sessions_collection.find_one({"_id": ObjectId(chat_id)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat session not found")

    # If it's the first message, update the title
    if not chat.get("messages"):
        trimmed_title = msg.text.strip()
        if len(trimmed_title) > 50:
            trimmed_title = trimmed_title[:47] + "..."
        chat_sessions_collection.update_one(
            {"_id": ObjectId(chat_id)},
            {"$set": {"title": trimmed_title}}
        )

    # Add the message and update last_interacted_at
    chat_sessions_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {
            "$push": {
                "messages": {
                    "sender": msg.sender,
                    "text": msg.text,
                    "sources": msg.sources or [],  # <-- Store sources if provided
                    "timestamp": datetime.utcnow()
                }
            },
            "$set": {
                "last_interacted_at": datetime.utcnow()
            }
        }
    )

    return {"message": "Message added"}


# Fetch messages from a specific chat
@router.get("/chats/{chat_id}/messages")
def get_messages(chat_id: str):
    session = chat_sessions_collection.find_one({"_id": ObjectId(chat_id)})
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"messages": session.get("messages", [])}


# Get all chat sessions for a specific user, sorted by recency
@router.get("/chats")
def get_user_chats(user_id: str):
    chats = chat_sessions_collection.find(
        {"user_id": user_id}
    ).sort("last_interacted_at", -1)
    response = [{"_id": str(chat["_id"]), "title": chat["title"]}
                for chat in chats]
    return {"sessions": response}


# Delete a chat
@router.delete("/chats/{chat_id}")
def delete_chat(chat_id: str):
    result = chat_sessions_collection.delete_one({"_id": ObjectId(chat_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"message": "Chat deleted"}