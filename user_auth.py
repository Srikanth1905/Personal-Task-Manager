import bcrypt
import sqlite3
import logging
from database import execute_query, fetch_query

def register_user(email, password, username):
    """
    Brief: Registers a new user in the system.
    Parameters:  email The email address of the user.
    Parameters:  password The password of the user.
    Parameters:  username The username of the user.
    Returns:  A message indicating the success or failure of the registration.
    Details:
    This function salts and hashes the password using bcrypt, then inserts the user's data into the database.
    If the email or username already exists, an error message is returned. Otherwise, the user is successfully registered.
    
    Example:
    Code
    message = register_user("user@example.com", "password123", "username")
    print(message)
    EndCode
    """
    try:
        # Salt and hash the password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)

        query = "INSERT INTO users (email, password, username) VALUES (?, ?, ?)"
        execute_query(query, (email, hashed_password, username))
        return "User registered successfully"
    except sqlite3.IntegrityError:
        return "Email or username already exists"
    except Exception as e:
        logging.error(f"An error occurred while registering the user: {e}")
        return "Registration failed"


def login_user(email, password):
    """
    Brief: Authenticates a user by verifying their email and password.
    Parameters:  email The email address of the user.
    Parameters:  password The password provided by the user.
    Returns:  The user's ID if authentication is successful, or None if authentication fails.
    Details:
    This function retrieves the user's hashed password from the database and compares it with the provided password.
    If the passwords match, the user's ID is returned. If the authentication fails, None is returned.
    
    Example:
    Code
    user_id = login_user("user@example.com", "password123")
    if user_id:
        print(f"Login successful for user ID: {user_id}")
    else:
        print("Invalid credentials")
    EndCode
    """
    query = "SELECT id, password FROM users WHERE email=?"
    result = fetch_query(query, (email,))

    if result:
        stored_hash = result[0][1]
        user_id = result[0][0]
        if bcrypt.checkpw(password.encode(), stored_hash):
            return user_id  # Return user ID on successful login
        else:
            return None  # Invalid password
    else:
        return None  # User not found


def get_user_by_email(email):
    """
    Brief: Retrieves a user's information from the database based on their email address.
    Parameters:  email The email address of the user.
    Returns:  A list of tuples, where each tuple represents a row in the 'users' table.
    Details:
    Executes a SQL query to select all columns from the 'users' table where the email matches the provided email address.
    If no user is found with the given email, an empty list is returned.
    
    Example:
    Code
    user_info = get_user_by_email("user@example.com")
    if user_info:
        print(f"User found: {user_info}")
    else:
        print("User not found")
    EndCode
    """
    query = "SELECT * FROM users WHERE email=?"
    return fetch_query(query, (email,))
