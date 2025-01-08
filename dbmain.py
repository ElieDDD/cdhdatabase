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
    except Exception as e:
        st.error(f"Error querying data: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Delete an entry from the database
def delete_entry(entry_id):
    try:
        conn = sqlite3.connect("university_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM university_data WHERE id = ?", (entry_id,))
        conn.commit()

        # Check if the deletion was successful
        if cursor.rowcount == 0:
            st.error(f"No record found with ID {entry_id}")
            conn.close()
            return False
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error deleting record: {str(e)}")
        return False

# Run a custom SQL query
def run_sql_query(query):
    try:
        conn = sqlite3.connect("university_data.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error running SQL query: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Main app
def main():
    st.title("University Database Interface")

    init_db()

    # Tabs for data entry and interrogation
    tab1, tab2, tab3 = st.tabs(["Add Data", "Query Data", "SQL Query"])

    # Add Data Tab
    with tab1:
        st.header("Add Data")
        university = st.text_input("University Name")
        duration = st.text_input("Duration")
        fee = st.text_input("Fee")
        themes = st.text_area("Themes (comma-separated)")
        comments = st.text_area("Comments")

        if st.button("Add Record"):
            if university and duration and fee and themes and comments:
                if insert_data(university, duration, fee, themes, comments):
                    st.success("Record added successfully!")
                else:
                    st.error("Failed to add record.")
            else:
                st.error("Please fill in all fields.")

    # Query Data Tab
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

                # Let the user select a record by ID for deletion
                selected_id = st.selectbox("Select the ID of the record to delete", result_df['id'].tolist())
                
                # Show the delete button only when an ID is selected
                if selected_id and st.button(f"Delete Record with ID {selected_id}"):
                    st.write(f"Attempting to delete record with ID: {selected_id}")
                    if delete_entry(selected_id):
                        st.success(f"Record with ID {selected_id} has been deleted.")
            else:
                st.write("No records found.")

    # SQL Query Tab
    with tab3:
        st.header("Run Custom SQL Query")
        query = st.text_area("Enter SQL Query (e.g., SELECT * FROM university_data)")
        
        if st.button("Run Query"):
            if query.strip():
                result_df = run_sql_query(query)
                if not result_df.empty:
                    st.dataframe(result_df)
                else:
                    st.write("No data returned or error in query.")
            else:
                st.error("Please enter a SQL query.")

if __name__ == "__main__":
    main()
