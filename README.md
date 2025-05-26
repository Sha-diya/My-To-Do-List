## Project Overview

**ToDoApp_app** is a Django-based application for managing personal tasks. It supports user authentication and allows users to create, view, update, complete, and delete their to-do tasks. Tasks can be filtered by their status and due date.

---

## Key Functionalities

### 1. **User Authentication**
- **Registration:** Users can register with a username, email, and password. Password confirmation is required.
- **Login/Logout:** Users can log in and log out securely.
- **Custom Forms:** Uses customized Django forms for registration and login, providing a user-friendly interface.

### 2. **Task Management**
- **Task Model:** Each task is linked to a user and has a title, due date, and completion status.
- **Task List:** Users can view a list of their tasks after logging in.
- **Add Task:** Users can add new tasks with a title and an optional due date.
- **Update Task:** Tasks can be edited to change their title and due date.
- **Complete Task:** Users can mark tasks as completed.
- **Delete Task:** Tasks can be deleted from the list.

### 3. **Task Filtering**
- **Today’s Tasks:** View tasks due today.
- **Pending Tasks:** View future, incomplete tasks.
- **Overdue Tasks:** View incomplete tasks with a past due date.
- **All Tasks:** View all tasks, filterable by status using different URLs.

### 4. **AJAX/JSON Support**
- **Update Completion (AJAX):** Task completion status can be updated via AJAX for a smoother user experience, returning a JSON response.

### 5. **Security**
- **Login Required:** Most task-related actions require the user to be logged in.
- **CSRF Exemption:** AJAX endpoint for updating completion is CSRF-exempt (note: should be secured for production).

---

## Main URLs

- `/` – Login page
- `/register/` – User registration
- `/tasks` – View all tasks
- `/add/` – Add a new task
- `/complete/<task_id>/` – Mark task as complete
- `/delete/<task_id>/` – Delete a task
- `/update/<task_id>/` – Edit a task
- `/filter/<filter_type>/` – Filter tasks (today, pending, overdue, etc.)
- `/update-task-completion/` – Update completion status via AJAX

---

