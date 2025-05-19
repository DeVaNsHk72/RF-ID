import streamlit as st
import sqlite3

st.set_page_config(page_title="RFID Library System", layout="wide")
st.title("📚 RFID Library Dashboard")

conn = sqlite3.connect("library.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT student_id, book_id, issue_time FROM issued_books")
records = cursor.fetchall()

st.subheader("Currently Issued Books")
st.table(records)
