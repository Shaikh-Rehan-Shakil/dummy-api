# Dummy HR API

Minimal HR employee-management API built with Flask, SQLite, and SQLAlchemy. The app auto-creates the database, seeds demo data, and exposes CRUD-style endpoints for employees, departments, attendance, leaves, and mock authentication.

## Prerequisites

- Python 3.13 (pipenv installs its own environment)
- `pipenv`

## Getting Started

### Using helper scripts (e.g. on Render)

```bash
/home/niko/Coding/dummy-api/scripts/build.sh   # pip install -r requirements.txt
/home/niko/Coding/dummy-api/scripts/start.sh   # python -m flask run (honors $HOST/$PORT)
```

### Manual steps (local dev with pipenv)

```bash
cd /home/niko/Coding/dummy-api
pipenv install
pipenv run flask --app app run --reload
```

The server listens on `http://127.0.0.1:5000`. Tables and demo data are created on first boot inside `hr.db`.

## Project Structure

```
app.py               # Flask application factory + health check
db.py                # SQLAlchemy instance
models/              # ORM models
routes/              # Blueprint modules per resource
seed_data.py         # One-time seeding logic
README.md
```

## Example cURL Requests

```bash
# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "maya.chen@example.com", "password": "password123"}'

# Current user (set header to employee id)
curl http://localhost:5000/auth/me -H "X-User-ID: 3"

# List employees
curl http://localhost:5000/employees

# Create employee
curl -X POST http://localhost:5000/employees \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Ivy","last_name":"Reid","email":"ivy.reid@example.com","department_id":2,"role":"QA Engineer"}'

# Employee leave balances (includes sick/vacation/maternity usage & eligibility)
curl http://localhost:5000/employees/3/leave-summary

# Submit leave request
curl -X POST http://localhost:5000/leaves \
  -H "Content-Type: application/json" \
  -d '{"employee_id":1,"start_date":"2025-12-15","end_date":"2025-12-16","reason":"Conference"}'

# List leave requests for one employee
curl "http://localhost:5000/leaves?employee_id=1"

# Approve leave
curl -X PATCH http://localhost:5000/leaves/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"approved"}'

# Check-in
curl -X POST http://localhost:5000/attendance/check-in \
  -H "Content-Type: application/json" \
  -d '{"employee_id":2}'

# Departments
curl http://localhost:5000/departments
```

## Notes

- Authentication is intentionally simple and not production-grade.
- Use the `X-User-ID` header to mimic a logged-in employee for `/auth/me`.
- Update `app.py` for different DB locations or to disable debug mode.
- Employee responses now include `leave_balances` describing sick, vacation, and (when applicable) maternity totals, days used, remaining, and eligibility.
- After pulling schema changes, delete `hr.db` so Flask can recreate tables with the new leave-balance columns and seeded attendance data.

