"""
@file app.py
@brief A Streamlit app for task management.

This module contains the implementation of the Task Ninja Streamlit application, 
including user authentication, task management dashboard, and task CRUD operations.
It provides a user-friendly interface for managing tasks efficiently.
"""

import streamlit as st
import datetime
from task import (
    add_task_with_status, update_task_with_status, delete_task, 
    get_tasks_by_user_id, get_task_by_id,
    get_tasks_by_status
)
from user_auth import login_user, register_user
from database import  create_tables, execute_query, fetch_query

create_tables()

# Page Configuration
st.set_page_config(page_title="Task Ninja 🥷", page_icon="✅", layout="wide")

# Authentication State Management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.edit_task_id = None
    st.session_state.show_task_form = False

if 'show_task_form' not in st.session_state:
    st.session_state.show_task_form = False

def login_page():
    """
    Displays the login and registration pages for the Task Ninja application.

    Allows users to:
    - Log in with their credentials.
    - Register for a new account.
    Handles session state changes for user authentication.
    """
    st.title("🥷 Task Ninja: Your Productivity Companion")

    col1, col2 = st.columns(2)

    with col1:
        st.header("🔐 Login")
        login_email = st.text_input("📧 Email", key="login_email")
        login_password = st.text_input("🔑 Password", type="password", key="login_password")

        if st.button("Login", type="primary"):
            user_id = login_user(login_email, login_password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.rerun()
            else:
                st.error("Invalid credentials")

    with col2:
        st.header("📝 Register")
        register_username = st.text_input("👤 Username", key="register_username")
        register_email = st.text_input("📧 Email", key="register_email")
        register_password = st.text_input("🔑 Password", type="password", key="register_password")

        if st.button("Register", type="secondary"):
            result = register_user(register_email, register_password, register_username)
            if result == "User registered successfully":
                st.success("Registration Successful!")
            else:
                st.error(result)

def task_dashboard():
    """
    Displays the task management dashboard for authenticated users.

    Includes:
    - A sidebar to filter tasks by status.
    - A list of tasks with options to view, edit, delete, or update their status.
    - A form to add or edit tasks.
    """
    st.title(f"📋 Task Dashboard")
    
    # Sidebar for Filters
    st.sidebar.header("🎛️ Task Status")
    status_filter = st.sidebar.selectbox("Filter by Status", ["All", "Pending", "To Do", "In Progress", "Completed"])
    
    # Add Task Button
    if st.sidebar.button("➕ Add New Task"):
        st.session_state.show_task_form = True
        st.session_state.edit_task_id = None
    
    # Main Task Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🚀 Your Tasks")
        
        # Apply Status Filter
        if status_filter == "All":
            tasks = get_tasks_by_user_id(st.session_state.user_id)
        else:
            tasks = get_tasks_by_status(status_filter)
        
        # Task Display
        if tasks:
            for task in tasks:
                with st.expander(f"{task[2]} - 🏷️ {task[5]} Priority - Status: {task[7]}"):
                    st.markdown(f"**Description:** {task[3]}")
                    st.markdown(f"**Due Date:** {task[4]}")
    
                    col_edit, col_delete, col_status = st.columns(3)
                    with col_edit:
                        if st.button(f"Edit Task", key=f"edit_{task[0]}"):
                            st.session_state.edit_task_id = task[0]
                            st.session_state.show_task_form = True
                            st.rerun()

                    with col_delete:
                        if st.button(f"Delete Task", key=f"delete_{task[0]}"):
                            delete_task(task[0])
                            st.rerun()
                    
                    with col_status:
                        new_status = st.selectbox(
                            "Change Status", 
                            ["Pending", "To Do", "In Progress", "Completed"], key=f"status_{task[0]}",
                            index=["Pending", "To Do", "In Progress", "Completed"].index(task[7])
                        )
                        if new_status != task[7]:
                            update_task_with_status(task[0], task[2], task[3], task[4], task[5], new_status)
                            st.rerun()
        else:
            st.info("No tasks found. Create your first task!")
    
    # Task Form (Only shows when Add or Edit is triggered)
    if st.session_state.show_task_form:
        with col2:
            st.header("➕ Add/Edit Task")
            with st.form("task_form", clear_on_submit=True):
                # Edit Mode
                if st.session_state.edit_task_id:
                    current_task = get_task_by_id(st.session_state.edit_task_id)
                    
                    if current_task is None:
                        st.error("Task not found. Please refresh the page.")
                        st.session_state.edit_task_id = None
                        st.session_state.show_task_form = False
                        st.rerun()
                    else:
                        title = st.text_input("Task Title", value=current_task[2])
                        description = st.text_area("Description", value=current_task[3])
                        due_date = st.date_input("Due Date", value=datetime.datetime.strptime(current_task[4], "%Y-%m-%d").date())
                        priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(current_task[5]))
                        status = st.selectbox("Status", ["Pending", "To Do", "In Progress", "Completed"], index=["Pending", "To Do", "In Progress", "Completed"].index(current_task[7]))
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.form_submit_button("Update Task"):
                                update_task_with_status(st.session_state.edit_task_id, title, description, str(due_date), priority, status)
                                st.session_state.edit_task_id = None
                                st.session_state.show_task_form = False
                                st.rerun()
                        
                        with col2:
                            if st.form_submit_button("Cancel"):
                                st.session_state.edit_task_id = None
                                st.session_state.show_task_form = False
                                st.rerun()
                
                # Add New Task Mode
                else:
                    title = st.text_input("Task Title")
                    description = st.text_area("Description")
                    due_date = st.date_input("Due Date")
                    priority = st.selectbox("Priority", ["Low", "Medium", "High"])
                    status = st.selectbox("Status", ["Pending", "To Do", "In Progress", "Completed"])
                    
                    if st.form_submit_button("Add Task"):
                        add_task_with_status(st.session_state.user_id, title, description, str(due_date), priority, status)
                        st.session_state.show_task_form = False
                        st.rerun()

def main():
    """
    The main function that manages the app flow.

    If the user is logged in:
    - Displays the task dashboard.
    If not:
    - Displays the login page.

    Includes a logout button to manage user sessions.

    """
    if not st.session_state.logged_in:
        login_page()
    else:
        task_dashboard()
        # Logout button in sidebar
        if st.sidebar.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.edit_task_id = None
            st.session_state.show_task_form = False
            st.rerun()

if __name__ == "__main__":
    main()
