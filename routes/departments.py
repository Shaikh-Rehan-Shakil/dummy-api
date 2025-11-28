from flask import Blueprint, jsonify, request

from db import db
from models import Department

departments_bp = Blueprint("departments", __name__)


@departments_bp.get("")
def list_departments():
    departments = Department.query.all()
    return jsonify({"departments": [dept.to_dict() for dept in departments]})


@departments_bp.post("")
def create_department():
    payload = request.get_json() or {}
    name = (payload.get("name") or "").strip()
    description = payload.get("description")

    if not name:
        return jsonify({"error": "Department name is required."}), 400

    if Department.query.filter_by(name=name).first():
        return jsonify({"error": "Department already exists."}), 409

    department = Department(name=name, description=description)
    db.session.add(department)
    db.session.commit()

    return jsonify({"department": department.to_dict()}), 201

