from fastapi import FastAPI, Request
import sqlite3

app = FastAPI()

@app.post("/rfid-scan")
async def scan_rfid(request: Request):
    data = await request.json()
    student_id = data.get("student_id")
    book_id = data.get("book_id")

    if not student_id or not book_id:
        return {"status": "error", "message": "Missing student or book ID"}

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS issued_books (student_id TEXT, book_id TEXT, issue_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
    cursor.execute("SELECT * FROM issued_books WHERE book_id = ?", (book_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("DELETE FROM issued_books WHERE book_id = ?", (book_id,))
        conn.commit()
        return {"status": "returned", "book_id": book_id}
    else:
        cursor.execute("INSERT INTO issued_books (student_id, book_id) VALUES (?, ?)", (student_id, book_id))
        conn.commit()
        return {"status": "issued", "book_id": book_id, "student_id": student_id}
