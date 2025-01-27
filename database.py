import sqlite3
from typing import Any

def get_db_connection():
    """
    Establishes a connection to the SQLite database 'task_manager.db' and sets the row factory to sqlite3.Row.

    Returns:
        sqlite3.Connection: A connection object to the SQLite database.
    """
    conn = sqlite3.connect('task_manager.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """
    Creates the necessary tables for the application in the database if they do not already exist.
    This function establishes a connection to the database, creates a cursor, and executes SQL
    statements to create the following tables:
    - users: Stores user information including id, username, email, password, and created_at timestamp.
    - tasks: Stores task information including id, user_id, title, description, due_date, priority,
      created_at timestamp, status, and a foreign key reference to the users table.
    After executing the SQL statements, the function commits the changes and closes the database connection.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE NOT NULL,
            priority TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    
    conn.commit()
    conn.close()
