from dotenv import load_dotenv
import os

# Only load .env in dev; on Render, vars come from the environment
if os.getenv("RENDER") != "true":
    load_dotenv() 

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
