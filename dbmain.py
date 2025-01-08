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
    conn = sqlite3.connect("university_data.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO university_data (university, duration, fee, themes, comments)
        VALUES (?, ?, ?, ?, ?)
    ''', (university, duration, fee, themes, comments))
    conn.commit()
    conn.close()

# Query data from database
def query_data(filters):
    conn = sqlite3.connect("university_data.db")
    query = "SELECT * FROM university_data WHERE 1=1"

    # Apply filters dynamically
    for key, value in filters.items():
        if value:
            if key == "themes":
                query += f" AND {key} LIKE '%{value}%'"
            else:
                query += f" AND {key} = '{value}'"

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Delete an entry from the database
def delete_entry(entry_id):
    conn = sqlite3.connect("university_data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM university_data WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

# Main app
def main():
    st.title("University Database Interface")

    init_db()

    # Tabs for data entry and interrogation
    tab1, tab2 = st.tabs(["Add Data", "Query Data"])

    with tab1:
        st.header("Add Data")
        university = st.text_input("University Name")
        duration = st.text_input("Duration")
        fee = st.text_input("Fee")
        themes = st.text_area("Themes (comma-separated)")
        comments = st.text_area("Comments")

        if st.button("Add Record"):
            if university and duration and fee and themes and comments:
                insert_data(university, duration, fee, themes, comments)
                st.success("Record added successfully!")
            else:
                st.error("Please fill in all fields.")

    with tab2:
        st.header("Query Data")
        st.write("Use the filters below to search the database:")

        filter_university = st.text_input("Filter by University")
        filter_duration = st.text_input("Filter by Duration")
        filter_fee = st.text_input("Filter by Fee")
        filter_themes = st.text_input("Filter by Themes (keyword)")

        filters = {
            "university": filter_university,
            "duration": filter_duration,
            "fee": filter_fee,
            "themes": filter_themes,
        }

        if st.button("Search"):
            result_df = query_data(filters)
            if not result_df.empty:
                st.dataframe(result_df)

                # Allow deletion of records
                selected_id = st.number_input("Enter the ID of the record to delete", min_value=1, step=1)
                if st.button("Delete Record"):
                    delete_entry(selected_id)
                    st.success(f"Record with ID {selected_id} has been deleted.")
            else:
                st.write("No records found.")

if __name__ == "__main__":
    main()
