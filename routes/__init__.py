from flask import Blueprint

from routes.attendance import attendance_bp
from routes.auth import auth_bp
from routes.departments import departments_bp
from routes.employees import employees_bp
from routes.leaves import leaves_bp

api_bp = Blueprint("api", __name__)

api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(employees_bp, url_prefix="/employees")
api_bp.register_blueprint(leaves_bp, url_prefix="/leaves")
api_bp.register_blueprint(attendance_bp, url_prefix="/attendance")
api_bp.register_blueprint(departments_bp, url_prefix="/departments")

