#  Finance Dashboard Backend

##  About

This project is a backend system built for managing financial records and generating dashboard insights.

The goal was to design something **simple, clean, and practical**, where different users can interact with financial data based on their roles, while also getting useful insights like income, expenses, and trends.

---

## Features

###  User Management

* Create users with roles:

  * **Viewer** → can only access dashboard
  * **Analyst** → can view records and insights
  * **Admin** → full access (create, update, delete)
* Prevents duplicate users (email/username)

---

###  Financial Records

* Add income/expense entries
* Update or delete records (**Admin only**)
* Fetch records with filters:

  * type (income / expense)
  * category
  * date range
* Handles edge cases like:

  * no records found
  * invalid updates

---

### Dashboard Insights

* Total income
* Total expenses
* Net balance
* Category-wise totals
* Recent activity
* Monthly trends

All data is **user-specific**, ensuring no data leakage.

---

###  Role-Based Access Control (RBAC)

Access is enforced at the backend level:

| Role    | Permissions              |
| ------- | ------------------------ |
| Viewer  | Dashboard only           |
| Analyst | View records + dashboard |
| Admin   | Full access              |

RBAC is implemented directly in the service logic to keep the system simple and readable.

---

###  Validation & Error Handling

* Duplicate user validation
* Clear and meaningful error messages
* Safe database operations
* Handles invalid or missing data gracefully

---

## Project Structure

```id="proj_tree"
app/
├── router/        # API routes
├── rq_rs/         # Request & response schemas
├── services/      # Business logic
├── models/        # Table definitions
├── constants/     # Roles & status
├── config.py
├── db.py
└── main.py
```

---

## Tech Stack

* **FastAPI** → backend framework
* **SQLite** → database
* **SQLAlchemy Core** → database interaction
* **Pydantic** → validation

---

##  Data Persistence

The project uses **SQLite** for simplicity and quick setup.

* Data is stored in a local file (`finance.db`)
* Tables:

  * `users`
  * `records`

⚠ Note: Since SQLite is file-based, when deployed on platforms like Render (which are stateless), data may reset on redeploy.

For production use, this can be replaced with PostgreSQL or MySQL.

---

##  How to Run

### 1. Create virtual environment

```id="cmd1"
python -m venv venv
```

### 2. Activate it

**Windows**

```id="cmd2"
venv\Scripts\activate
```

**Mac/Linux**

```id="cmd3"
source venv/bin/activate
```

---

### 3. Install dependencies

```id="cmd4"
pip install -r requirements.txt
```

---

### 4. Initialize database

```id="cmd5"
python init_db.py
```

---

### 5. Run the server

```id="cmd6"
uvicorn app.main:app --reload
```

---

## API Endpoints

###  Users

* `POST /users/create_user`

### Records

* `POST /records/create_record`
* `POST /records/fetch_records`
* `PUT /records/update_record`
* `DELETE /records/delete_record`

###  Dashboard

* `POST /dashboard/summary`
* `POST /dashboard/category`
* `POST /dashboard/recent`
* `POST /dashboard/trends`

---

## Design Choices

* Kept routers simple and moved logic into utils
* Used function-based structure instead of overengineering
* Focused on readability and maintainability
* Implemented RBAC at service level



---

##  Final Note

This project was built to demonstrate:

* backend design thinking
* handling real-world scenarios
* writing clean and maintainable, reusable  code

The focus was on building something that is **easy to understand and works reliably**, rather than adding unnecessary complexity.

---
