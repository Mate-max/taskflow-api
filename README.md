# 🚀 TaskFlow API

A secure, high-performance RESTful Task Management Backend built with **FastAPI**, **SQLAlchemy ORM**, and **MS SQL Server**, featuring JWT-based authentication.

---

## 🛠️ Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
* **Database & ORM:** MS SQL Server, SQLAlchemy, Pyodbc
* **Authentication:** OAuth2 with Password Bearer, JWT Tokens (`python-jose`), Passlib (`bcrypt`)
* **Data Validation:** Pydantic v2

---

## ✨ Features

* **User Management & Auth:** Secure user registration and token-based login (JWT) with password hashing.
* **Full CRUD Operations:** Create, Read, Update, and Delete tasks via protected endpoints.
* **User Isolation / Ownership:** Users can only view, update, and delete their own tasks (`owner_id` relational binding).
* **Interactive Documentation:** Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## ⚙️ Quick Start & Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Mate-max/taskflow-api.git](https://github.com/Mate-max/taskflow-api.git)
   cd taskflow-api

   python -m venv venv
# On Windows:
venv\Scripts\activate

 ## Install dependencies
pip install fastapi uvicorn sqlalchemy pyodbc pydantic passlib[bcrypt]==3.2.2 python-jose

Configure Database Connection:
Ensure your MS SQL Server (.\SQLEXPRESS) is running and create a database named TaskFlowDB. Update your connection string in database.py:

SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://@.\SQLEXPRESS/TaskFlowDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

## Run the Application:
uvicorn main:app --reload

## 📌 API Endpoints Overview

| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Register a new user | Public |
| `POST` | `/token` | Login and obtain JWT Access Token | Public |
| `GET` | `/tasks` | Retrieve all tasks for the logged-in user | Protected |
| `POST` | `/tasks` | Create a new task | Protected |
| `PUT` | `/tasks/{id}` | Update an existing task | Protected |
| `DELETE` | `/tasks/{id}` | Delete a task | Protected |

👨‍💻 Author
Mate Askilashvili
