from datetime import datetime

from flask import Blueprint, jsonify, request

from db import db
from models import Employee, LeaveRequest

leaves_bp = Blueprint("leaves", __name__)


@leaves_bp.get("")
def list_leaves():
    employee_id_param = request.args.get("employee_id")

    if employee_id_param is not None:
        try:
            employee_id = int(employee_id_param)
        except ValueError:
            return jsonify({"error": "employee_id must be an integer."}), 400

        employee = Employee.query.get(employee_id)
        if not employee:
            return jsonify({"error": "Employee not found."}), 404

        leaves = LeaveRequest.query.filter_by(employee_id=employee_id).all()
    else:
        leaves = LeaveRequest.query.all()

    return jsonify({"leaves": [leave.to_dict() for leave in leaves]})


@leaves_bp.post("")
def create_leave():
    payload = request.get_json() or {}
    errors = _validate_leave_payload(payload, creation=True)
    if errors:
        return jsonify({"errors": errors}), 400

    leave = LeaveRequest(
        employee_id=payload["employee_id"],
        start_date=_to_date(payload["start_date"]),
        end_date=_to_date(payload["end_date"]),
        reason=payload.get("reason"),
        status="pending",
    )
    db.session.add(leave)
    db.session.commit()

    return jsonify({"leave": leave.to_dict()}), 201


@leaves_bp.get("/<int:leave_id>")
def get_leave(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    return jsonify({"leave": leave.to_dict()})


@leaves_bp.patch("/<int:leave_id>")
def update_leave(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    payload = request.get_json() or {}

    if "status" in payload:
        status = payload["status"].lower()
        if status not in {"pending", "approved", "rejected"}:
            return jsonify({"error": "Status must be pending, approved, or rejected."}), 400
        leave.status = status

    if "start_date" in payload:
        leave.start_date = _to_date(payload["start_date"])

    if "end_date" in payload:
        leave.end_date = _to_date(payload["end_date"])

    if "reason" in payload:
        leave.reason = payload["reason"]

    db.session.commit()
    return jsonify({"leave": leave.to_dict()})


def _validate_leave_payload(payload, creation=False):
    errors = []
    employee_id = payload.get("employee_id")
    start_date = payload.get("start_date")
    end_date = payload.get("end_date")

    if creation and not employee_id:
        errors.append("employee_id is required.")
    if creation and not start_date:
        errors.append("start_date is required.")
    if creation and not end_date:
        errors.append("end_date is required.")

    if employee_id and not Employee.query.get(employee_id):
        errors.append("employee_id is invalid.")

    try:
        if start_date:
            _ = _to_date(start_date)
        if end_date:
            _ = _to_date(end_date)
    except ValueError:
        errors.append("Dates must be in YYYY-MM-DD format.")

    if start_date and end_date:
        start = _to_date(start_date)
        end = _to_date(end_date)
        if start > end:
            errors.append("start_date must be on or before end_date.")

    return errors


def _to_date(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date()
    return value

