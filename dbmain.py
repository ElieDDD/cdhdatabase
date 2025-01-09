import('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
#import sqlite3
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

# Run a custom SQL query
def run_sql_query(query):
    try:
        conn = sqlite3.connect("university_data.db")
        # Return the result as a pandas DataFrame
        if query.strip().lower().startswith('select'):
            df = pd.read_sql_query(query, conn)
        else:
            conn.execute(query)
            conn.commit()
            df = pd.DataFrame()  # For non-SELECT queries, no result set is returned
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error running SQL query: {str(e)}")
        return pd.DataFrame()  # return empty dataframe on error

# Reset the auto-increment counter
'''def reset_auto_increment():
    try:
        conn = sqlite3.connect("university_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='university_data';")
        conn.commit()
        conn.close()
        st.success("Auto-increment counter reset successfully!")
    except Exception as e:
        st.error(f"Error resetting auto-increment counter: {str(e)}")
'''
# Main app
def main():
    st.title("Data Schools Database")

    init_db()

    # Tabs for data entry, querying data, and SQL query
    tab1, tab2, tab3 = st.tabs(["Add Data", "Query Data", "SQL Query"])

    # Add Data Tab
    with tab1:
        st.header("Add Data")
        university = st.text_input("University Name")
        duration = st.text_input("Duration")
        fee = st.text_input("Fee")
        themes = st.text_area("Themes (comma-separated)")
        comments = st.text_area("Comments")  # Re-added comment area

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

        # Reset Auto-Increment Counter Button
        #if st.button("Reset Auto-Increment Counter"):
           #reset_auto_increment()

if __name__ == "__main__":
    main()
