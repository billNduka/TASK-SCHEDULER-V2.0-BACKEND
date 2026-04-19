# Task Scheduler v2.0 Backend

A FastAPI-based backend for a task scheduling application with user authentication, task management, and advanced features like recurrence and progress tracking.

## Features

- **User Authentication**: Register and login with JWT tokens.
- **Task Management**: Create, read, update, delete tasks.
- **Advanced Task Features**:
  - Categories, due dates, descriptions.
  - Recurring tasks (daily, weekly, monthly).
  - Progress tracking with quotas.
  - Subtasks support.
  - Email reminders (framework in place).
- **API Documentation**: Auto-generated Swagger UI at `/docs`.
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Security**: Bcrypt password hashing, JWT authentication.

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (local or hosted)
- Git

### Setup
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd TASK-SCHEDULER-V2.0-BACKEND
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Install PostgreSQL locally or use a hosted service (e.g., Supabase).
   - Create a database named `taskscheduler`.
   - Create a user `taskuser` with password `secret` (or update `.env` accordingly).

5. Configure environment variables:
   - Copy `.env.example` to `.env` (if provided) or create `.env`:
     ```env
     DATABASE_URL=postgresql://taskuser:secret@localhost:5432/taskscheduler
     SECRET_KEY=your_secret_key_here
     ```
   - Generate a strong `SECRET_KEY` (e.g., use `openssl rand -hex 32`).

6. Run the application:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. Access the app:
   - API: `http://127.0.0.1:8000`
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Usage

### API Endpoints
- **Auth**:
  - `POST /auth/register`: Register a new user.
  - `POST /auth/login`: Login and get JWT token.
- **Tasks** (requires Bearer token in `Authorization` header):
  - `GET /tasks/`: List all tasks for the user.
  - `GET /tasks/{task_id}`: Get a specific task.
  - `POST /tasks/`: Create a new task.
  - `PUT /tasks/{task_id}`: Update a task.
  - `DELETE /tasks/{task_id}`: Delete a task.
  - `PATCH /tasks/{task_id}`: Update task completion progress (query param `amount`).

### Example API Calls
Use curl or tools like Postman:

1. Register:
   ```bash
   curl -X POST "http://127.0.0.1:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
   ```

2. Login:
   ```bash
   curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'
   ```
   Returns: `{"access_token": "...", "token_type": "bearer"}`

3. Create Task (use token from login):
   ```bash
   curl -X POST "http://127.0.0.1:8000/tasks/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <your_token>" \
     -d '{"title": "My Task", "description": "Task description"}'
   ```

4. Get Tasks:
   ```bash
   curl -X GET "http://127.0.0.1:8000/tasks/" \
     -H "Authorization: Bearer <your_token>"
   ```

## Project Structure
```
TASK-SCHEDULER-V2.0-BACKEND/
├── main.py                 # FastAPI app entry point
├── database.py             # Database configuration
├── models/
│   └── models.py           # SQLAlchemy models
├── schemas/
│   ├── user.py             # User Pydantic schemas
│   └── task.py             # Task Pydantic schemas
├── controllers/
│   ├── auth_controllers.py # Auth logic
│   └── task_controllers.py # Task logic
├── routers/
│   ├── auth_routes.py      # Auth routes
│   └── task_routes.py      # Task routes
├── core/
│   └── security.py         # Security utilities
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version
├── .env                    # Environment variables (not in repo)
└── README.md               # This file
```

## Development
- **Linting**: Install `pylint` and run `pylint .` for code quality.
- **Testing**: Add unit tests with `pytest`.
- **Database Migrations**: Use Alembic for schema changes (not implemented yet).

## Contributing
1. Fork the repo.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push and create a PR.

## License
MIT License. See LICENSE file for details.

## Contact
For issues or questions, open a GitHub issue.
