from typing import Optional
from database import get_db_connection
import sqlite3
import bcrypt
import re

def validate_user(username: str, password: str) -> Optional[int]:
    """
    Validates a user's credentials against the database.
    Args:
        username (str): The username of the user.
        password (str): The password of the user.
    Returns:
        Optional[int]: The user ID if the credentials are valid, otherwise None.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            user_id, hashed_password = result
            if bcrypt.checkpw(password.encode(), hashed_password):
                return user_id
        return None
    finally:
        conn.close()
    
def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed_password: bytes) -> bool:
    """
    Verify if the provided password matches the hashed password.

    Args:
        password (str): The plain text password to verify.
        hashed_password (bytes): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

def register_user(email: str, password: str, username: str) -> str:
    """
    Registers a new user in the database.
    Args:
        email (str): The email address of the user.
        password (str): The password for the user account.
        username (str): The username for the user account.
    Returns:
        str: A message indicating the result of the registration process.
            - "Email already registered" if the email is already in use.
            - "User registered successfully" if the registration is successful.
            - "Registration error: <error_message>" if an error occurs during registration.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return "Email already registered"
        
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (email, password, username) VALUES (?, ?, ?)",(email, hashed_password, username))
        conn.commit()
        return "User registered successfully"
    except Exception as e:
        return f"Registration error: {str(e)}"
    finally:
        conn.close()

def login_user(email: str, password: str) -> Optional[int]:
    """
    Authenticates a user by their email and password.
    Args:
        email (str): The email address of the user.
        password (str): The password provided by the user.
    Returns:
        Optional[int]: The user ID if authentication is successful, otherwise None.
    """
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE name = ?", (email,))
        result = cursor.fetchone()
        
        if result:
            user_id, hashed_password = result
            if verify_password(password, hashed_password):
                return user_id
        return None
    finally:
        conn.close()


