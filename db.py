import sqlite3
from typing import List, Optional
from models import Category, Task


class DB:
    def __init__(self, path="database.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                done INTEGER NOT NULL DEFAULT 0,
                category_id INTEGER,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            )
        """)
        self.conn.commit()

    def add_category(self, name: str) -> int:
        name = name.strip()
        if not name:
            raise ValueError("Nome vazio")

        cur = self.conn.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        self.conn.commit()
        return cur.lastrowid

    def get_categories(self) -> List[Category]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM categories ORDER BY name")
        rows = cur.fetchall()
        return [Category(row["id"], row["name"]) for row in rows]

    def update_category(self, category_id: int, name: str):
        name = name.strip()
        if not name:
            raise ValueError("Nome vazio")
        cur = self.conn.cursor()
        cur.execute("UPDATE categories SET name=? WHERE id=?", (name, category_id))
        self.conn.commit()

    def delete_category(self, category_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM categories WHERE id=?", (category_id,))
        self.conn.commit()

    def add_task(self, title: str, description: str, category_id: Optional[int]) -> int:
        title = title.strip()
        if not title:
            raise ValueError("Título vazio")

        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO tasks (title, description, done, category_id)
            VALUES (?, ?, 0, ?)
        """, (title, description, category_id))
        self.conn.commit()
        return cur.lastrowid

    def get_tasks(self) -> List[Task]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks ORDER BY id DESC")
        rows = cur.fetchall()
        return [
            Task(
                row["id"],
                row["title"],
                row["description"] or "",
                bool(row["done"]),
                row["category_id"]
            )
            for row in rows
        ]

    def get_task(self, task_id: int) -> Optional[Task]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
        row = cur.fetchone()
        if row:
            return Task(row["id"], row["title"], row["description"], bool(row["done"]), row["category_id"])
        return None

    def update_task(self, task_id: int, title: str, description: str, done: bool, category_id: Optional[int]):
        title = title.strip()
        if not title:
            raise ValueError("Título vazio")

        cur = self.conn.cursor()
        cur.execute("""
            UPDATE tasks SET title=?, description=?, done=?, category_id=? WHERE id=?
        """, (title, description, int(done), category_id, task_id))
        self.conn.commit()

    def delete_task(self, task_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


def seed_if_empty(db: DB):
    if not db.get_categories():
        c1 = db.add_category("Pessoal")
        c2 = db.add_category("Trabalho")
        c3 = db.add_category("Estudos")

        db.add_task("Comprar leite", "Ir ao mercado", c1)
        db.add_task("Enviar relatório", "Enviar por e-mail", c2)
        db.add_task("Estudar SQL", "Praticar JOINs", c3)