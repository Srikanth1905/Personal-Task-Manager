from typing import List, Tuple, Optional
from database import get_db_connection

def add_task_with_status(user_id: int, title: str, description: str, due_date: str, priority: str, status: str):
    """
    Adds a new task with the given details to the database and returns the task ID.

    Args:
        user_id (int): The ID of the user to whom the task belongs.
        title (str): The title of the task.
        description (str): A detailed description of the task.
        due_date (str): The due date of the task in the format 'YYYY-MM-DD'.
        priority (str): The priority level of the task (e.g., 'low', 'medium', 'high').
        status (str): The current status of the task (e.g., 'pending', 'completed').

    Returns:
        int: The ID of the newly created task.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tasks (user_id, title, description, due_date, priority, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, title, description, due_date, priority, status))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def update_task_with_status(task_id: int, title: str, description: str, due_date: str, priority: str, status: str):
    """
    Update the details of a task in the database with the given status.

    Args:
        task_id (int): The ID of the task to update.
        title (str): The new title of the task.
        description (str): The new description of the task.
        due_date (str): The new due date of the task in 'YYYY-MM-DD' format.
        priority (str): The new priority of the task.
        status (str): The new status of the task.

    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tasks 
        SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
        WHERE id = ?
    """, (title, description, due_date, priority, status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id: int):
    """
    Deletes a task from the database based on the provided task ID.

    Args:
        task_id (int): The ID of the task to be deleted.

    Returns:
        None
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def get_tasks_by_user_id(user_id: int) -> List[Tuple]:
    """
    Retrieve tasks for a specific user from the database.

    Args:
        user_id (int): The ID of the user whose tasks are to be retrieved.

    Returns:
        List[Tuple]: A list of tuples, each representing a task. The tasks are ordered by their due date in ascending order.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def get_task_by_id(task_id: int) -> Optional[Tuple]:
    """
    Retrieve a task from the database by its ID.

    Args:
        task_id (int): The ID of the task to retrieve.

    Returns:
        Optional[Tuple]: A tuple containing the task data if found, otherwise None.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task

def get_tasks_by_status(user_id: int, status: str) -> List[Tuple]:
    """
    Retrieve tasks for a specific user filtered by status and ordered by due date.

    Args:
        user_id (int): The ID of the user whose tasks are to be retrieved.
        status (str): The status of the tasks to filter by (e.g., 'completed', 'pending').

    Returns:
        List[Tuple]: A list of tuples representing the tasks that match the given user ID and status,
                     ordered by their due date in ascending order.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY due_date ASC",
        (user_id, status)
    )
    tasks = cursor.fetchall()
    conn.close()
    return tasks


