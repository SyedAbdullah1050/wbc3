import streamlit as st
import sqlite3
import pandas as pd

# Function to initialize the database
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task TEXT, priority TEXT, completed INTEGER)''')
    conn.commit()
    conn.close()

# Function to add a task to the database
def add_task(task, priority):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, priority, completed) VALUES (?, ?, ?)", (task, priority, 0))
    conn.commit()
    conn.close()

# Function to delete a task from the database
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# Function to mark a task as completed
def mark_completed(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed=1 WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# Function to retrieve tasks from the database
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    tasks_df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()
    return tasks_df

# Main function to run the Streamlit app
def main():
    init_db()
    st.title("Routine Management API")

    # Sidebar to perform actions
    st.sidebar.title("Actions")
    action = st.sidebar.selectbox("Select Action", ["Add Task", "Delete Task", "Mark Completed", "View Tasks"])

    if action == "Add Task":
        new_task = st.text_input("Enter new task:")
        priority = st.selectbox("Select priority", ["Low", "Medium", "High"])
        if st.button("Add"):
            add_task(new_task, priority)
            st.success("Task added successfully!")

    elif action == "Delete Task":
        tasks_df = get_tasks()
        task_id = st.selectbox("Select task to delete:", tasks_df["task"])
        if st.button("Delete"):
            delete_task(task_id)
            st.success("Task deleted successfully!")

    elif action == "Mark Completed":
        tasks_df = get_tasks()
        task_id = st.selectbox("Select task to mark as completed:", tasks_df["task"])
        if st.button("Mark"):
            mark_completed(task_id)
            st.success("Task marked as completed!")

    elif action == "View Tasks":
        tasks_df = get_tasks()
        st.write("### Your Tasks:")
        st.dataframe(tasks_df)

if __name__ == "__main__":
    main()
