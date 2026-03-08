"""
Script: app.py
Description: FastAPI application with VULNERABLE SQL query (for educational purposes)
"""
from __future__ import annotations
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
DB_PATH = "/app/data/users.db"

def init_db():
    """Создаём тестовую базу данных"""
    os.makedirs("/app/data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    
    test_users = [
        ('admin', 'admin@example.com', 'admin'),
        ('john', 'john@example.com', 'user'),
        ('alice', 'alice@example.com', 'user'),
        ('bob', 'bob@example.com', 'manager')
    ]
    
    for user in test_users:
        try:
            cursor.execute(
                "INSERT INTO users (username, email, role) VALUES (?, ?, ?)",
                user
            )
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
    logger.info("✅ Database initialized")

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    class Config:
        from_attributes = True

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/users/{username}")
def get_user(username: str):
    """🔴 VULNERABLE: SQL Injection possible"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ⚠️ УЯЗВИМОСТЬ: конкатенация строк!
    query = f"SELECT * FROM users WHERE username = '{username}'"
    logger.info(f"📄 Executing: {query}")
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [{"id": r[0], "username": r[1], "email": r[2], "role": r[3]} for r in results]

@app.get("/search")
def search_users(username: str = Query(...)):
    """🔴 VULNERABLE: SQL Injection possible"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = f"SELECT * FROM users WHERE username = '{username}'"
    logger.info(f"📄 Executing: {query}")
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    users = [{"id": r[0], "username": r[1], "email": r[2], "role": r[3]} for r in results]
    return {"query": query, "users": users, "message": f"Found {len(users)} user(s)"}

@app.get("/users_secure/{username}")
def get_user_secure(username: str):
    """✅ SECURE: Using parameterized queries"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ✅ БЕЗОПАСНО: параметризованный запрос
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [{"id": r[0], "username": r[1], "email": r[2], "role": r[3]} for r in results]