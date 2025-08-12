import os
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3
import pandas as pd

load_dotenv()

def run_nl_query(question):
    # Get API key from .env
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # Create Groq-compatible OpenAI client
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    # Path to your SQLite DB
    db_path = os.path.join("data", "sqlite-sakila.db")

    # Prompt for SQL generation
    prompt = f"""
    You are an expert in translating natural language questions into SQL for SQLite databases.
    Database name: sakila.
    Question: {question}
    Respond ONLY with the SQL query, nothing else.
    """

    # Call Groq API
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # ✅ Correct Groq model name
        messages=[
            {"role": "system", "content": "You convert natural language questions into SQL for SQLite."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    sql_query = response.choices[0].message.content.strip()  # ✅ fixed here

    # Run SQL query on database
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql_query, conn)
    finally:
        conn.close()

    return df
