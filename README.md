# issuee_tracker
```markdown
# FastAPI Issue Tracker Backend

This is the backend for an Issue Tracker application built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It provides REST APIs for creating, updating, filtering, and listing issues.

---

## Features

- Create, read, update, and delete issues.
- Filter issues by status, priority, and assignee.
- Pagination and sorting support.
- CORS enabled for frontend integration.

---

## Tech Stack

- **Python 3.10+**
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pydantic**
- **Uvicorn**
- **Databases**
- **python-dotenv** for environment variables

---

## Folder Structure

```

backend/
├── main.py           # FastAPI app entrypoint
├── models.py         # SQLAlchemy models
├── database.py       # DB connection
├── requirements.txt  # Python dependencies
└── .env              # Environment variables (DB URL, etc.)

````

---

## Setup Locally

1. Clone the repository:

```bash
git clone <your-repo-url>
cd backend
````

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the FastAPI server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. Access API docs at:

```
http://localhost:8000/docs
```

---

## Deployment on Railway

1. Create a new project on [Railway](https://railway.app/).
2. Connect your GitHub repository.
3. Set environment variables in Railway (DATABASE\_URL, etc.).
4. Set the **Start Command**:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

5. Deploy. Railway will assign a dynamic port and host.

---

## API Endpoints

* `GET /issues` → List issues with optional filters, pagination, and sorting.
* `POST /issues` → Create a new issue.
* `GET /issues/{id}` → Get issue details.
* `PUT /issues/{id}` → Update an issue.
* `DELETE /issues/{id}` → Delete an issue.

---


