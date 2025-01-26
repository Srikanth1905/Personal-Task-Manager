from database import execute_query, fetch_query

def add_task_with_status(user_id, title, description, due_date, priority, status):
    """
    Adds a new task with the given details to the database.

    Parameters:

    user_id (int): The unique identifier of the user who created the task.
    title (str): The title of the task.
    description (str): The description of the task.
    due_date (str): The due date of the task in the format 'YYYY-MM-DD'.
    priority (int): The priority of the task (1 being the highest priority).
    status (str): The status of the task ('pending', 'in progress', 'completed').

    Returns:
    None
    """
    query = """
    INSERT INTO tasks (user_id, title, description, due_date, priority, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """
    values = (user_id, title, description, due_date, priority, status)
    execute_query(query, values)


def update_task_with_status(task_id, title, description, due_date, priority, status):
    """
Updates a task in the database with the given status and other details.

This function updates the specified task's title, description, due date, priority, and status
in the 'tasks' table of the task management database.

Parameters:
task_id (int): The ID of the task to be updated.
title (str): The new title of the task.
description (str): The new description of the task.
due_date (str): The new due date of the task.
priority (int): The new priority level of the task.
status (str): The new status of the task.

Returns:
None
"""
    query = '''
    UPDATE tasks
    SET title = ?, description = ?, due_date = ?, priority = ?, status = ?
    WHERE id = ?
    '''
    execute_query(query, (title, description, due_date, priority, status, task_id))

def delete_task(task_id):
    """
Deletes a task from the task management database.

This function removes a task from the 'tasks' table based on the provided task ID.

Parameters:
task_id (int): The ID of the task to be deleted.

Returns:
None
"""
    query = "DELETE FROM tasks WHERE id = ?"
    execute_query(query, (task_id,))

def get_tasks_by_user_id(user_id):
    """
Retrieve tasks associated with a specific user ID from the database.

This function constructs a SQL query to select all tasks for a given user ID
and uses the fetch_query function to execute the query and return the results.

Parameters:
user_id (int): The ID of the user whose tasks are to be retrieved.

Returns:
list: A list of tuples, where each tuple represents a task associated with the user.
"""
    query = "SELECT * FROM tasks WHERE user_id = ?"
    return fetch_query(query, (user_id,))

def get_task_by_id(task_id):
    """
Retrieve a task from the database by its ID.

This function executes a SQL query to fetch a task from the 'tasks' table
using the provided task ID. It returns the first result if found, otherwise
returns None.

Parameters:
task_id (int): The ID of the task to retrieve.

Returns:
tuple or None: A tuple representing the task if found, otherwise None.
"""
    query = "SELECT * FROM tasks WHERE id = ?"
    results =  fetch_query(query, (task_id,))
    return results[0] if results else None

def get_tasks_by_priority(priority):
    """
Fetches tasks from the database based on the specified priority.

This function executes a SQL query to retrieve all tasks with the given priority
from the 'tasks' table in the task management database.

Parameters:
priority (int): The priority level of the tasks to be fetched.

Returns:
list: A list of tuples, where each tuple represents a task with the specified priority.
"""
    query = "SELECT * FROM tasks WHERE priority = ?"
    return fetch_query(query, (priority,))

def get_tasks_by_due_date(due_date):
    """
Fetches tasks from the database with the specified due date.

This function executes a SQL query to retrieve all tasks that have a due date
matching the provided `due_date` parameter.

Parameters:
due_date (str): The due date to filter tasks by.

Returns:
list: A list of tuples, where each tuple represents a task with the specified due date.
"""
    query = "SELECT * FROM tasks WHERE due_date = ?"
    return fetch_query(query, (due_date,))

def get_tasks_by_date_range(start_date, end_date):
    """
Fetches tasks within a specified date range from the database.

This function executes a SQL query to retrieve all tasks whose due dates
fall between the given start and end dates.

Parameters:
start_date (str): The start date of the range in 'YYYY-MM-DD' format.
end_date (str): The end date of the range in 'YYYY-MM-DD' format.

Returns:
list: A list of tuples representing the tasks within the specified date range.
"""
    query = "SELECT * FROM tasks WHERE due_date BETWEEN ? AND ?"
    return fetch_query(query, (start_date, end_date))

def get_tasks_by_title_or_description(search_term):
    """
Fetches tasks from the database that match the given search term in their title or description.

This function constructs a SQL query to search for tasks where the title or description contains
the specified search term. It utilizes the fetch_query function to execute the query and retrieve
the matching tasks.

Parameters:
search_term (str): The term to search for in the task titles and descriptions.

Returns:
list: A list of tuples representing the tasks that match the search criteria.
"""
    query = "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?"
    return fetch_query(query, (f"%{search_term}%", f"%{search_term}%"))

def set_priority(priority, task_id):
    """
Updates the priority of a task in the database.

This function updates the priority of a task identified by its ID in the 'tasks' table
of the task management database.

Parameters:
priority (int): The new priority level to be set for the task.
task_id (int): The ID of the task whose priority is to be updated.

Returns:
str: A confirmation message indicating the priority was updated successfully.
"""
    query = "UPDATE tasks SET priority = ? WHERE id = ?"
    execute_query(query, (priority, task_id))
    return "Priority updated successfully"

def set_due_date(due_date, task_id):
    """
Updates the due date of a task in the database.

This function updates the 'due_date' field of a task identified by 'task_id'
in the 'tasks' table of the task management database.

Parameters:
due_date (str): The new due date to be set for the task.
task_id (int): The ID of the task whose due date is to be updated.

Returns:
str: A confirmation message indicating the due date was updated successfully.
"""
    query = "UPDATE tasks SET due_date = ? WHERE id = ?"
    execute_query(query, (due_date, task_id))
    return "Due date updated successfully"

def set_title(title, task_id):
    """
Updates the title of a task in the database.

This function updates the title of a task identified by its task ID in the 'tasks' table.

Parameters:
title (str): The new title for the task.
task_id (int): The ID of the task to update.

Returns:
str: A confirmation message indicating the title was updated successfully.
"""
    query = "UPDATE tasks SET title = ? WHERE id = ?"
    execute_query(query, (title, task_id))
    return "Title updated successfully"

def set_description(description, task_id):
    """
Updates the description of a task in the database.

This function updates the description of a task identified by its task ID
in the 'tasks' table of the database.

Parameters:
description (str): The new description for the task.
task_id (int): The ID of the task to update.

Returns:
str: A confirmation message indicating the update was successful.
"""
    query = "UPDATE tasks SET description = ? WHERE id = ?"
    execute_query(query, (description, task_id))
    return "Description updated successfully"

def get_tasks_by_status(status):
    """
Fetches tasks from the database based on their status.

This function executes a SQL query to retrieve all tasks with the specified status
from the 'tasks' table in the task management database.

Parameters:
status (str): The status of the tasks to be fetched.

Returns:
list: A list of tuples, where each tuple represents a task with the specified status.
"""
    query = "SELECT * FROM tasks WHERE status = ?"
    return fetch_query(query, (status,))