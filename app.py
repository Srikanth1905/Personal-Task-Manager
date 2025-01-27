
"""This script implements a task management web application using Streamlit. The application allows users to register, log in, and manage their tasks. The main features include:
User authentication (registration and login)
Task creation, editing, deletion, and status updates
Task filtering by status
Display of task metrics (total tasks, completed tasks, remaining tasks)
Modules and functions:
`validate_email(email: str) -> bool`: Validates an email address.
`validate_password(password: str) -> bool`: Validates a password to ensure it meets the required criteria.
`auth_pages()`: Handles the user authentication pages (registration and login).
`task_form_page()`: Handles the task creation/editing form.
`task_dashboard()`: Creates a task dashboard with controls for filtering tasks by status, displaying metrics, and allowing users to add, edit, delete, and update task statuses.
`main()`: The main function that sets up the Streamlit page configuration, initializes the database tables, and manages the navigation between authentication and task management pages.
The script uses the following external modules:
`streamlit`: For creating the web application interface.
`datetime`: For handling date and time operations.
`re`: For regular expression operations.
`database`: Custom module for database operations.
`user_auth`: Custom module for user authentication operations.
`task`: Custom module for task management operations.
The script initializes session states to manage user authentication and navigation between different pages of the application."""

from datetime import datetime
import streamlit as st
from database import create_tables
from user_auth import register_user, login_user,validate_user
from task import (
    add_task_with_status, update_task_with_status, delete_task,
    get_tasks_by_user_id, get_task_by_id, get_tasks_by_status
)
import re
st.set_page_config(page_title="Task Ninja 🥷", page_icon="✅", layout="wide")
# Initialize session states
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'edit_task_id' not in st.session_state:
    st.session_state['edit_task_id'] = None
if 'show_task_form' not in st.session_state:
    st.session_state['show_task_form'] = False
if 'auth_page' not in st.session_state:
    st.session_state['auth_page'] = "login"
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "dashboard"

def validate_email(email: str) -> bool:
    """
     Validates an email address.
 
     Args:
         email (str): The email address to validate.
 
     Returns:
         bool: True if the email address is valid, False otherwise.
   """

    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def validate_password(password: str) -> bool:
    """
    Validates a password to ensure it meets the required criteria.

    Parameters:
    password (str): The password to validate.

    Returns:
    bool: True if the password meets the criteria, False otherwise.
          The criteria are: minimum length of 5 characters and at least one special character 
          from the set (!@#$%^&*()-+).
    """
    return len(password) >= 5 and any(char in "!@#$%^&*()-+" for char in password)



def auth_pages():
    """
    Displays the authentication pages (login and registration) for the Task Ninja application.
    The function checks the current state of the authentication page (login or register) and displays
    the appropriate form. It handles user input validation and provides feedback to the user.
    Registration Page:
    - Prompts the user to enter a username, email, and password.
    - Validates the input fields.
    - Registers the user if the input is valid and displays a success message.
    - Provides an option to switch to the login page.
    Login Page:
    - Prompts the user to enter a username and password.
    - Validates the input fields.
    - Logs in the user if the input is valid and displays a success message.
    - Provides an option to switch to the registration page.
    Note:
    - The function uses Streamlit for the UI components.
    - The function relies on external functions `validate_email`, `validate_password`, `register_user`, and `validate_user` for input validation and user management.
    Returns:
        None
    """

    st.title("🥷 Task Ninja: Your Productivity Companion")
    if st.session_state.get("auth_page", "login") == "register":
        # Registration page
        st.header("📝 Register")
        register_username = st.text_input("👤 Username", key="register_username")
        register_email = st.text_input("📧 Email", key="register_email")
        register_password = st.text_input("🔑 Password", type="password", key="register_password")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Register", type="primary"):

                if not register_username:
                    st.warning("Please enter a username.")
                elif not validate_email(register_email):
                    st.warning("Please enter a valid email address.")
                elif not validate_password(register_password):
                    st.warning("Password must be at least 5 characters long and contain a special character (!@#$%^&*()-+).")
                else:
                    result = register_user(register_email, register_password, register_username)
                    if result == "User registered successfully":
                        st.success("Registration successful! Please login.")
                        st.session_state.auth_page = "login"
                        st.rerun()
                    else:
                        st.error(result)

        with col2:
            st.markdown("Already have an account?")
            if st.button("Go to Login"):
                st.session_state.auth_page = "login"
                st.rerun()

    else:  
        st.header("🔐 Login")
        login_username = st.text_input("👤 Username", key="login_username")  
        login_password = st.text_input("🔑 Password", type="password", key="login_password")

        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Login", type="primary"):
                # Validate inputs
                if not login_username:
                    st.warning("Please enter a username.")
                elif not validate_password(login_password):
                    st.warning("Password must be at least 5 characters long and contain a special character (!@#$%^&*()-+).")
                else:
                    
                    user_id = validate_user(login_username, login_password)
                    if user_id:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user_id
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

        with col2:
            st.markdown("Don't have an account?")
            if st.button("Go to Register"):
                st.session_state.auth_page = "register"
                st.rerun()

def task_form_page():
    """
    Handle task creation and editing form.
    This function displays a form for creating a new task or editing an existing task.
    It handles the following functionalities:
    - Navigating back to the dashboard.
    - Displaying the form for editing a task if `edit_task_id` is set in the session state.
    - Displaying the form for adding a new task if `edit_task_id` is not set in the session state.
    - Updating an existing task with the provided details.
    - Adding a new task with the provided details.
    - Handling form submission and cancellation actions.
    The form includes fields for:
    - Task Title
    - Description
    - Due Date
    - Priority (Low, Medium, High)
    - Status (Pending, To Do, In Progress, Completed)
    The function also handles error cases such as task not found during editing and 
    exceptions during task update or addition.
    Raises:
        Exception: If there is an error updating or adding a task.
    """


    if st.button("← Back to Dashboard"):
        st.session_state.current_page = "dashboard"
        st.rerun()

    if st.session_state.edit_task_id:
        st.header("✏️ Edit Task")
        current_task = get_task_by_id(st.session_state.edit_task_id)
        
        if current_task is None:
            st.error("Task not found. Please return to dashboard.")
            st.session_state.edit_task_id = None
            st.session_state.current_page = "dashboard"
            st.rerun()
        
        with st.form("edit_task_form"):
            title = st.text_input("Task Title", value=current_task[2])
            description = st.text_area("Description", value=current_task[3])
            due_date = st.date_input("Due Date", 
                value=datetime.strptime(current_task[4], "%Y-%m-%d").date())
            priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                  index=["Low", "Medium", "High"].index(current_task[5]))
            status = st.selectbox("Status", 
                                ["Pending", "To Do", "In Progress", "Completed"],
                                index=["Pending", "To Do", "In Progress", "Completed"].index(current_task[7]))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Update Task"):
                    try:
                        update_task_with_status(st.session_state.edit_task_id, 
                                              title, description, str(due_date), 
                                              priority, status)
                        st.success("Task updated successfully!")
                        st.session_state.edit_task_id = None
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating task: {str(e)}")
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.edit_task_id = None
                    st.session_state.current_page = "dashboard"
                    st.rerun()
    
    else:
        st.header("➕ Add New Task")
        with st.form("add_task_form"):
            title = st.text_input("Task Title")
            description = st.text_area("Description")
            due_date = st.date_input("Due Date")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            status = st.selectbox("Status", ["Pending", "To Do", "In Progress", "Completed"])
            
            if st.form_submit_button("Add Task"):
                try:
                    add_task_with_status(st.session_state.user_id, title, description, 
                                       str(due_date), priority, status)
                    st.success("Task added successfully!")
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error adding task: {str(e)}")


def task_dashboard():
    """
    Displays the task dashboard in a Streamlit app.
    The dashboard includes:
    - A title.
    - A sidebar with controls to filter tasks by status and add new tasks.
    - Quick stats showing the total number of tasks, completed tasks, and remaining tasks.
    - A grid of task cards displaying task details and options to edit, delete, or change the status of each task.
    The function handles:
    - Fetching and filtering tasks based on the selected status filter.
    - Displaying metrics for total tasks, completed tasks, and remaining tasks.
    - Rendering task cards with task details and action buttons.
    - Handling actions such as editing, deleting, and updating task status.
    Raises:
        Exception: If there is an error loading tasks, an error message is displayed.
    """
    st.title("📋 Task Dashboard")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controls")
        status_filter = st.selectbox("Filter Status", 
            ["All", "Pending", "To Do", "In Progress", "Completed"])
        if st.button("➕ Add New Task", type="primary", use_container_width=True):
            st.session_state.edit_task_id = None
            st.session_state.current_page = "task_form"
            st.rerun()
    
    try:
        # Get and filter tasks
        tasks = (get_tasks_by_user_id(st.session_state.user_id) if status_filter == "All" 
                else get_tasks_by_status(st.session_state.user_id, status_filter))
        
        # Quick stats
        total = len(tasks)
        completed = sum(1 for t in tasks if t[7] == "Completed")
        
        # Display metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Tasks", total)
        m2.metric("Completed", completed)
        m3.metric("Remaining", total - completed)
        
        # Task cards in grid
        if tasks:
            st.markdown("---")
            for i in range(0, len(tasks), 2):
                col1, col2 = st.columns(2)
                cols = [col1, col2]
                
                for j in range(2):
                    if i + j < len(tasks):
                        task = tasks[i + j]
                        with cols[j]:
                            status_color = {
                                "Completed": "green",
                                "In Progress": "orange",
                                "To Do": "blue",
                                "Pending": "red"
                            }.get(task[7], "gray")

                            st.markdown(f"""
                                <div style='border: 1px solid #ddd; border-radius: 8px; padding: 10px;'>
                                    <h5 style='margin: 0;'>
                                        {task[2]} <span style='color:{status_color}; float:right;'>{task[7]}</span>
                                    </h5>
                                    <p style='margin: 5px 0;'>{task[3]}</p>
                                    <p><b>Due:</b> {task[4]} | <b>Priority:</b> {task[5]}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            c1, c2, c3 = st.columns([1,1,2])
                            with c1:
                                if st.button("✏️", key=f"edit_{task[0]}", help="Edit task details"):
                                    st.session_state.edit_task_id = task[0]
                                    st.session_state.current_page = "task_form"
                                    st.rerun()
                            with c2:
                                if st.button("🗑️", key=f"delete_{task[0]}", help="Delete Task"):
                                    delete_task(task[0])
                                    st.rerun()
                            with c3:
                                status_options = ["Pending", "To Do", "In Progress", "Completed"]
                                new_status = st.selectbox("Status", status_options,
                                    status_options.index(task[7]), key=f"status_{task[0]}",
                                    label_visibility="collapsed")
                                if new_status != task[7]:
                                    update_task_with_status(task[0], task[2], task[3],
                                        task[4], task[5], new_status)
                                    st.rerun()
        else:
            st.info("No tasks found. Create your first task!")
            
    except Exception as e:
        st.error(f"Error loading tasks: {str(e)}")

def main():
    """
    Main function to set up the Streamlit app configuration and handle user authentication and page navigation.
    This function performs the following tasks:
    1. Sets the page configuration with a title, icon, and layout.
    2. Creates necessary database tables.
    3. Checks if the user is logged in:
        - If not logged in, displays the authentication pages.
        - If logged in, navigates to the appropriate page based on the current page state.
    4. Provides a logout button in the sidebar to allow users to log out and reset session state.
    Session State Variables:
    - logged_in: Boolean indicating if the user is logged in.
    - current_page: String indicating the current page ("dashboard" or "task_form").
    - user_id: User's unique identifier.
    - edit_task_id: ID of the task being edited.
    - show_task_form: Boolean indicates whether the task form should be displayed.
    - auth_page: String indicating the current authentication page ("register" or other).
    Note:
    - The function uses Streamlit's session state to manage user authentication and page navigation.
    - The `st.rerun()` function is called to refresh the app when the user logs out.
    """
    
    create_tables()
    
    if not st.session_state['logged_in']:
        auth_pages()
    else:
        if st.session_state['current_page'] == "dashboard":
            task_dashboard()
        elif st.session_state['current_page'] == "task_form":
            task_form_page()

        if st.sidebar.button("🚪 Logout"):
            # Reset all session state variables
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            # Reinitialize with defaults
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['edit_task_id'] = None
            st.session_state['show_task_form'] = False
            st.session_state['auth_page'] = "login"
            st.session_state['current_page'] = "dashboard"
            st.rerun()
if __name__ == "__main__":
    main()
