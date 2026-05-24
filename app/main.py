from fastapi import FastAPI
import mysql.connector

app = FastAPI()

def get_connection():
    return mysql.connector.connect(
        host="mysql",
        user="root",
        password="rootpassword",
        database="mydb"
    )

@app.get("/")
def root():
    return {"message": "Python API + MySQL via Docker!"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": rows}
