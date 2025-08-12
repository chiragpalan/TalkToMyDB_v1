# app/query_engine.py
import os
import json
import sqlite3
from typing import Tuple
from openai import OpenAI
from .config import GROQ_API_KEY, GROQ_BASE_URL, GROQ_MODEL, SQLITE_PATH
from .vectorstore_client import retrieve_context
from .sql_validator import validate_sql

# create OpenAI-compatible client pointing to Groq
def _get_llm_client():
    if not GROQ_API_KEY:
        raise RuntimeError("Set GROQ_API_KEY in your .env or environment")
    client = OpenAI(base_url=GROQ_BASE_URL, api_key=GROQ_API_KEY)
    return client

def build_prompt(question: str, context_docs: list[str]) -> str:
    schema_ctx = "\n\n".join(context_docs)
    prompt = f"""
You are an expert SQLite assistant. Use the schema and descriptions below to write a safe SQL SELECT query to answer the user's question.
IMPORTANT: Return only the SQL query. Use standard SQLite syntax and include a LIMIT if appropriate.

Schema & notes:
{schema_ctx}

User question:
{question}

Answer (SQL):
"""
    return prompt

def generate_sql_from_llm(question: str, k=5) -> str:
    docs, metas = retrieve_context(question, k=k)
    prompt = build_prompt(question, docs)
    client = _get_llm_client()
    # Use chat completion style (OpenAI-compatible)
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful SQLite expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
        temperature=0.0
    )
    sql = resp.choices[0].message.content.strip()
    return sql

def get_results_for_question(question: str, db_path: str = None) -> dict:
    sql = generate_sql_from_llm(question)
    ok, reason = validate_sql(sql)
    if not ok:
        return {"error": f"Unsafe or invalid SQL generated: {reason}", "sql": sql}

    db_path = db_path or SQLITE_PATH
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
    except Exception as e:
        conn.close()
        return {"error": f"SQL execution error: {e}", "sql": sql}
    conn.close()
    return {"sql": sql, "columns": cols, "rows": rows}
