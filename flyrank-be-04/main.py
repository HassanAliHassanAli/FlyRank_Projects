from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

class PostgresRepo:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.conn.autocommit = True

    def add_user(self, name, role):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO users (name, role) VALUES (%s, %s) RETURNING id;", (name, role))
            return cur.fetchone()[0]

    def get_users(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, role FROM users;")
            return [{"id": row[0], "name": row[1], "role": row[2]} for row in cur.fetchall()]

repo = PostgresRepo()

@app.get("/")
def read_root():
    return {"status": "Postgres and FastAPI are connected!"}

@app.post("/users/")
def create_user(name: str, role: str):
    user_id = repo.add_user(name, role)
    return {"id": user_id, "name": name, "role": role}

@app.get("/users/")
def read_users():
    return repo.get_users()