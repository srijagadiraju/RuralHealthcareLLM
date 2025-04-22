from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.services.db import users_collection
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import re

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# === Schemas ===


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long")
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one uppercase letter")
    if not re.search(r"[a-zA-Z]", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one letter")
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number")
    if not re.search(r"[^a-zA-Z0-9]", password):
        raise HTTPException(
            status_code=400, detail="Password must include a special character")

# === Routes ===


@router.post("/signup")
def signup(user: UserCreate):
    validate_password_strength(user.password)
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    })

    return {"message": "User created successfully"}


@router.post("/login")
def login(user: UserLogin):
    db_user = users_collection.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(
            status_code=400, detail="Invalid email or password")

    if not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(
            status_code=400, detail="Invalid email or password")

    # Generate JWT token
    payload = {
        "sub": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    # Return name too (make sure name is stored in the user document during signup)
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": db_user.get("name", ""), "user_id": str(db_user["_id"])
    }
