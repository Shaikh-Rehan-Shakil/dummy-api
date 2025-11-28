from datetime import date, datetime

from db import db


class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Department(db.Model, TimestampMixin):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255))

    employees = db.relationship("Employee", back_populates="department", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Employee(db.Model, TimestampMixin):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(120))
    gender = db.Column(db.String(20), nullable=False, default="unspecified")
    password = db.Column(db.String(128), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=False)
    hire_date = db.Column(db.Date, nullable=False, default=date.today)
    sick_leave_total = db.Column(db.Integer, nullable=False, default=10)
    sick_leave_used = db.Column(db.Integer, nullable=False, default=0)
    vacation_leave_total = db.Column(db.Integer, nullable=False, default=15)
    vacation_leave_used = db.Column(db.Integer, nullable=False, default=0)
    maternity_leave_total = db.Column(db.Integer, nullable=False, default=0)
    maternity_leave_used = db.Column(db.Integer, nullable=False, default=0)

    department = db.relationship("Department", back_populates="employees")
    attendances = db.relationship("AttendanceRecord", back_populates="employee", lazy=True)
    leaves = db.relationship("LeaveRequest", back_populates="employee", lazy=True)

    def _build_leave_bucket(self, total, used):
        remaining = max(total - used, 0)
        return {
            "total": total,
            "used": used,
            "remaining": remaining,
            "eligible": remaining > 0,
        }

    def leave_balances(self):
        sick = self._build_leave_bucket(self.sick_leave_total, self.sick_leave_used)
        vacation = self._build_leave_bucket(
            self.vacation_leave_total, self.vacation_leave_used
        )
        maternity_total = self.maternity_leave_total if self.gender == "female" else 0
        maternity_used = (
            self.maternity_leave_used if self.gender == "female" else 0
        )
        maternity = self._build_leave_bucket(maternity_total, maternity_used)
        maternity["eligible"] = self.gender == "female" and maternity["remaining"] > 0

        return {
            "sick": sick,
            "vacation": vacation,
            "maternity": maternity,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "gender": self.gender,
            "department": self.department.to_dict() if self.department else None,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "leave_balances": self.leave_balances(),
        }


class AttendanceRecord(db.Model, TimestampMixin):
    __tablename__ = "attendance_records"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    check_in = db.Column(db.DateTime, nullable=False)
    check_out = db.Column(db.DateTime)

    employee = db.relationship("Employee", back_populates="attendances")

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "check_in": self.check_in.isoformat() if self.check_in else None,
            "check_out": self.check_out.isoformat() if self.check_out else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class LeaveRequest(db.Model, TimestampMixin):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255))
    status = db.Column(db.String(50), nullable=False, default="pending")

    employee = db.relationship("Employee", back_populates="leaves")

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "reason": self.reason,
            "status": self.status,
            "employee": {
                "id": self.employee.id,
                "first_name": self.employee.first_name,
                "last_name": self.employee.last_name,
            }
            if self.employee
            else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

