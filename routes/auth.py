from flask import Blueprint, jsonify, request

from models import Employee

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
def login():
    payload = request.get_json() or {}
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password") or ""

    if not email or not password:
        return (
            jsonify({"error": "Email and password are required."}),
            400,
        )

    user = Employee.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"error": "Invalid credentials."}), 401

    return jsonify({"user": user.to_dict()})


@auth_bp.get("/me")
def me():
    user_id = request.headers.get("X-User-ID")
    if not user_id:
        return jsonify({"error": "Missing X-User-ID header."}), 400

    user = Employee.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    user_payload = user.to_dict()
    user_payload.pop("leave_balances", None)
    return jsonify({"user": user_payload})

