from datetime import datetime, date

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError

from db import db
from models import Department, Employee

employees_bp = Blueprint("employees", __name__)

ALLOWED_GENDERS = {"female", "male", "non-binary", "unspecified"}
LEAVE_NUMERIC_FIELDS = [
    "sick_leave_total",
    "sick_leave_used",
    "vacation_leave_total",
    "vacation_leave_used",
    "maternity_leave_total",
    "maternity_leave_used",
]


@employees_bp.get("")
def list_employees():
    employees = Employee.query.all()
    return jsonify({"employees": [emp.to_dict() for emp in employees]})


@employees_bp.post("")
def create_employee():
    payload = request.get_json() or {}
    errors = _validate_employee_payload(payload, creation=True)
    if errors:
        return jsonify({"errors": errors}), 400

    gender = _normalize_gender(payload.get("gender"))
    employee = Employee(
        first_name=payload["first_name"].strip(),
        last_name=payload["last_name"].strip(),
        email=payload["email"].strip().lower(),
        role=payload.get("role"),
        gender=gender,
        password=payload.get("password") or "password123",
        department_id=payload["department_id"],
        hire_date=_parse_date(payload.get("hire_date")) if payload.get("hire_date") else date.today(),
        sick_leave_total=_coerce_int(payload.get("sick_leave_total"), 10),
        sick_leave_used=_coerce_int(payload.get("sick_leave_used"), 0),
        vacation_leave_total=_coerce_int(payload.get("vacation_leave_total"), 15),
        vacation_leave_used=_coerce_int(payload.get("vacation_leave_used"), 0),
        maternity_leave_total=_maternity_value(payload.get("maternity_leave_total"), gender),
        maternity_leave_used=_maternity_value(payload.get("maternity_leave_used"), gender),
    )
    db.session.add(employee)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists."}), 409

    return jsonify({"employee": employee.to_dict()}), 201


@employees_bp.get("/<int:employee_id>")
def get_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify({"employee": employee.to_dict()})


@employees_bp.get("/<int:employee_id>/leave-summary")
def get_employee_leave_summary(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return jsonify({"leave_summary": employee.leave_balances()})


@employees_bp.patch("/<int:employee_id>")
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    payload = request.get_json() or {}

    if "first_name" in payload:
        if not payload["first_name"].strip():
            return jsonify({"error": "First name cannot be empty."}), 400
        employee.first_name = payload["first_name"].strip()

    if "last_name" in payload:
        if not payload["last_name"].strip():
            return jsonify({"error": "Last name cannot be empty."}), 400
        employee.last_name = payload["last_name"].strip()

    if "email" in payload:
        email = payload["email"].strip().lower()
        if not email:
            return jsonify({"error": "Email cannot be empty."}), 400
        email_exists = (
            Employee.query.filter(Employee.email == email, Employee.id != employee.id)
            .with_entities(Employee.id)
            .first()
        )
        if email_exists:
            return jsonify({"error": "Email already in use."}), 409
        employee.email = email

    if "role" in payload:
        employee.role = payload["role"]

    if "gender" in payload:
        employee.gender = _normalize_gender(payload.get("gender"))
        if employee.gender != "female":
            employee.maternity_leave_total = 0
            employee.maternity_leave_used = 0

    if "department_id" in payload:
        department = Department.query.get(payload["department_id"])
        if not department:
            return jsonify({"error": "Department not found."}), 404
        employee.department_id = department.id

    for field in LEAVE_NUMERIC_FIELDS:
        if field not in payload:
            continue
        if field.startswith("maternity") and employee.gender != "female":
            setattr(employee, field, 0)
            continue
        current = getattr(employee, field)
        setattr(
            employee,
            field,
            _coerce_int(payload.get(field), current),
        )

    db.session.commit()
    return jsonify({"employee": employee.to_dict()})


def _validate_employee_payload(payload, creation=False):
    errors = []

    first_name = (payload.get("first_name") or "").strip()
    last_name = (payload.get("last_name") or "").strip()
    email = (payload.get("email") or "").strip()
    department_id = payload.get("department_id")
    gender = payload.get("gender")

    if creation and not first_name:
        errors.append("First name is required.")
    if creation and not last_name:
        errors.append("Last name is required.")
    if creation and not email:
        errors.append("Email is required.")
    if creation and not department_id:
        errors.append("Department id is required.")

    if email and "@" not in email:
        errors.append("Email must be valid.")

    if department_id:
        department = Department.query.get(department_id)
        if not department:
            errors.append("Department not found.")

    if gender:
        normalized_gender = gender.strip().lower()
        if normalized_gender not in ALLOWED_GENDERS:
            errors.append("Gender must be female, male, non-binary, or unspecified.")

    numeric_values = {}
    for field in LEAVE_NUMERIC_FIELDS:
        value = payload.get(field)
        if value is None:
            continue
        try:
            numeric_values[field] = int(value)
        except (TypeError, ValueError):
            errors.append(f"{field} must be an integer.")
            continue
        if numeric_values[field] < 0:
            errors.append(f"{field} cannot be negative.")

    _validate_leave_usage_limits(errors, numeric_values, "sick")
    _validate_leave_usage_limits(errors, numeric_values, "vacation")
    _validate_leave_usage_limits(errors, numeric_values, "maternity")

    return errors


def _parse_date(value):
    if not value:
        return date.today()
    if isinstance(value, date):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


def _normalize_gender(value):
    gender = (value or "unspecified").strip().lower()
    return gender if gender in ALLOWED_GENDERS else "unspecified"


def _coerce_int(value, default):
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _validate_leave_usage_limits(errors, numeric_values, prefix):
    total_key = f"{prefix}_leave_total"
    used_key = f"{prefix}_leave_used"
    if used_key not in numeric_values:
        return
    used = numeric_values[used_key]
    total = numeric_values.get(total_key)
    if total is not None and used > total:
        errors.append(f"{used_key} cannot exceed {total_key}.")


def _maternity_value(value, gender):
    if gender != "female":
        return 0
    return _coerce_int(value, 0)

