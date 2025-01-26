import sqlite3
import logging
from contextlib import closing

DATABASE_NAME = 'task_manager.db'

def create_tables():
    """
    This function creates the necessary tables for the task management system.

    The tables created are:
    1. 'users' table: Stores user information such as id, username, email, and password.
    2. 'tasks' table: Stores task information such as id, user_id (foreign key referencing users), title, description, due_date, priority, and status.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )""")

    # Create tasks table with status included
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")

    conn.commit()
    conn.close()
    print("Tables created successfully")


def execute_query(query, params=()):
    """
    Executes a SQL query on the task management database.

    This function connects to the SQLite database 'task_manager.db', executes the given SQL query with the provided parameters,
    and commits the changes. If an error occurs during the execution, it logs the error message and raises the exception.

    Parameters:
    query (str): The SQL query to be executed.
    params (tuple, optional): The parameters to be used in the SQL query. Defaults to an empty tuple.

    Returns:
    None

    Raises:
    sqlite3.Error: If an error occurs while executing the SQL query.
    """
    try:
        with closing(sqlite3.connect(DATABASE_NAME)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, params)
                conn.commit()
    except sqlite3.Error as e:
        logging.error(f"An error occurred while executing query: {e}")
        raise


def fetch_query(query, params=()):
    """
    Executes a SQL query on the task management database and fetches the result.

    This function connects to the SQLite database 'task_manager.db', executes the given SQL query with the provided parameters,
    fetches all the rows returned by the query, and returns them. If an error occurs during the execution, it logs the error message
    and returns an empty list.

    Parameters:
    query (str): The SQL query to be executed.
    params (tuple, optional): The parameters to be used in the SQL query. Defaults to an empty tuple.

    Returns:
    list: A list of tuples, where each tuple represents a row fetched from the database. If an error occurs, returns an empty list.

    Raises:
    sqlite3.Error: If an error occurs while executing the SQL query.
    """
    try:
        with closing(sqlite3.connect(DATABASE_NAME)) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                return rows
    except sqlite3.Error as e:
        logging.error(f"An error occurred while fetching data: {e}")
        return []


def modify_tasks_table():
    """
    Modifies the 'tasks' table in the task management database by adding a 'status' column if it does not exist.

    The function connects to the SQLite database 'task_manager.db', retrieves the column names from the 'tasks' table using
    the PRAGMA table_info() function, and checks if the 'status' column is present. If the 'status' column does not exist,
    the function adds the 'status' column with a default value of 'Pending' using the ALTER TABLE statement.

    Parameters:
    None

    Returns:
    None

    Raises:
    sqlite3.Error: If an error occurs while connecting to the database or executing SQL queries.
    """
    conn = sqlite3.connect('task_manager.db')
    cursor = conn.cursor()

    # Add status column if not exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'status' not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Pending'")

    conn.commit()
    conn.close()
