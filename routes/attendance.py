from datetime import datetime

from flask import Blueprint, jsonify, request

from db import db
from models import AttendanceRecord, Employee

attendance_bp = Blueprint("attendance", __name__)


@attendance_bp.post("/check-in")
def check_in():
    payload = request.get_json() or {}
    employee_id = payload.get("employee_id")
    timestamp = payload.get("timestamp")

    if not employee_id or not Employee.query.get(employee_id):
        return jsonify({"error": "Valid employee_id is required."}), 400

    dt = _parse_datetime(timestamp) if timestamp else datetime.utcnow()
    open_record = AttendanceRecord.query.filter_by(
        employee_id=employee_id, check_out=None
    ).first()
    if open_record:
        return jsonify({"error": "Employee already checked in."}), 400

    record = AttendanceRecord(employee_id=employee_id, check_in=dt)
    db.session.add(record)
    db.session.commit()

    return jsonify({"attendance": record.to_dict()}), 201


@attendance_bp.post("/check-out")
def check_out():
    payload = request.get_json() or {}
    employee_id = payload.get("employee_id")
    timestamp = payload.get("timestamp")

    if not employee_id or not Employee.query.get(employee_id):
        return jsonify({"error": "Valid employee_id is required."}), 400

    record = AttendanceRecord.query.filter_by(
        employee_id=employee_id, check_out=None
    ).order_by(AttendanceRecord.check_in.desc()).first()
    if not record:
        return jsonify({"error": "No active check-in found."}), 400

    dt = _parse_datetime(timestamp) if timestamp else datetime.utcnow()
    if dt < record.check_in:
        return jsonify({"error": "Check-out cannot be before check-in."}), 400

    record.check_out = dt
    db.session.commit()

    return jsonify({"attendance": record.to_dict()})


@attendance_bp.get("/<int:employee_id>")
def list_attendance(employee_id):
    if not Employee.query.get(employee_id):
        return jsonify({"error": "Employee not found."}), 404

    records = AttendanceRecord.query.filter_by(employee_id=employee_id).all()
    return jsonify({"records": [record.to_dict() for record in records]})


def _parse_datetime(value):
    if not value:
        raise ValueError("Invalid timestamp.")
    return datetime.fromisoformat(value)

