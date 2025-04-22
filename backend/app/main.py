from fastapi import FastAPI
from app.api.routes import router
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_routes  # NEW
from app.api import chat_routes  # NEW


app = FastAPI()

# Allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# New auth routes
app.include_router(auth_routes.router)
# new routes for saving chats
app.include_router(chat_routes.router)
