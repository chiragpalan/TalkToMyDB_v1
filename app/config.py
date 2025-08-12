# app/config.py
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env in project root if present

BASE_DIR = Path(__file__).resolve().parents[1]   # repo root /sakila-ai-app
DATA_DIR = BASE_DIR / "data"
VECTORS_DIR = BASE_DIR / "vectors"

# DB file path (adjust if different)
SQLITE_PATH = DATA_DIR / "sqlite-sakila.db"

# Groq / OpenAI-compatible settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set in .env
# OpenAI-compatible base URL for Groq:
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
# default model (you can change to a Groq-supported model)
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")  # example
