import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "shaktipeeth-secret-2024-xK9mP")

    # Fix for Render PostgreSQL
    db_url = os.environ.get("DATABASE_URL")

    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url or "sqlite:///shaktipeeth.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie settings — required for Render (HTTPS)
    SESSION_COOKIE_SECURE = os.environ.get("RENDER", False)  # True on Render, False locally
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Mail configuration (uses local defaults if env vars are missing on Render)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "jasolaaksh@gmail.com")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "uddymzrgolqhkrux")
    # URL for Ollama or external LLM API (default to local Ollama)
    OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/chat")
