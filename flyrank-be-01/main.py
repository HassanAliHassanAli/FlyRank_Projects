from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# --- النماذج (Models) ---
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str = None
    done: bool = None

# --- دوال قاعدة البيانات ---
def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Learn Python', 1)")
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Build API', 0)")
        cursor.execute("INSERT INTO tasks (title, done) VALUES ('Connect to SQLite', 0)")
    conn.commit()
    conn.close()

init_db()

# --- مسارات الـ API الأساسية ---
@app.get("/")
def read_root():
    return {"message": "Hello FlyRank, this is Hassan's first endpoint!"}

@app.get("/status")
def read_status():
    return {"status": "Active", "intern": "Builder level - Ready for Backend A"}

# === Stage 1: Read ===
@app.get("/tasks")
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return [dict(task) for task in tasks]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    conn = get_db_connection()
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(task)

# === Stage 2: Create ===
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (task.title, 0))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return {"id": task_id, "title": task.title, "done": False}

# === Stage 3: Update & Delete ===
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    existing_task = cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
    
    new_title = task.title if task.title is not None else existing_task['title']
    new_done = task.done if task.done is not None else existing_task['done']
    
    cursor.execute('UPDATE tasks SET title = ?, done = ? WHERE id = ?', (new_title, new_done, task_id))
    conn.commit()
    conn.close()
    return {"id": task_id, "title": new_title, "done": new_done}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    existing_task = cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if existing_task is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task deleted successfully"}