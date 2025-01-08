import streamlit as st
import sqlite3
import pandas as pd

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("university_data.db")
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS university_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university TEXT,
            duration TEXT,
            fee TEXT,
            themes TEXT,
            comments TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert data into database
def insert_data(university, duration, fee, themes, comments):
    try:
        conn = sqlite3.connect("university_data.db")
        cursor = conn.cursor()
        cursor.execute(''' 
            INSERT INTO university_data (university, duration, fee, themes, comments)
            VALUES (?, ?, ?, ?, ?)
        ''', (university, duration, fee, themes, comments))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error inserting record: {str(e)}")
        return False

# Query data from database
def query_data(filters):
    try:
        conn = sqlite3.connect("university_data.db")
        query = "SELECT * FROM university_data WHERE 1=1"

        # App
