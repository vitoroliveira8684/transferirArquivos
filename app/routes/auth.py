from fastapi import APIRouter, Request;
from fastapi.templating import Jinja2Templates;
import sqlite3;


router = APIRouter();

templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
def login_page(request: Request):
        return templates.TemplateResponse(
              request = request,
              name = "login.html",
              context = {
                    "request": request
              }
        )


conn = sqlite3.connect("database.db");

cursor = conn.cursor();


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE,
               hash_password TEXT
               )
               """)

user_data = ("Vitor", 30);
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", user_data);

conn.commit();

cursor.execute("SELECT * FROM users");

all_rows = cursor.fetchall();


for row in all_rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}");

conn.close();


