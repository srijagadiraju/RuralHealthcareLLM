from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_routes  # NEW
from app.api import chat_routes  # NEW

from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
# Serve React frontend

# Allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers with prefix
app.include_router(router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")
app.include_router(chat_routes.router, prefix="/api")

# Serve React frontend from built files
frontend_path = "/app/frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
