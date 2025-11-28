from datetime import date, datetime, timedelta

from db import db
from models import AttendanceRecord, Department, Employee, LeaveRequest


def seed_database():
    """Populate the database with deterministic demo data."""
    if Department.query.first():
        return

    departments = [
        Department(name="Human Resources", description="Hiring and people ops"),
        Department(name="Engineering", description="Product development"),
        Department(name="Sales", description="Revenue generation"),
        Department(name="Finance", description="Accounting and planning"),
    ]
    db.session.add_all(departments)
    db.session.flush()

    employees = [
        Employee(
            first_name="Ava",
            last_name="Stone",
            email="ava.stone@example.com",
            role="HR Manager",
            gender="female",
            password="password123",
            department_id=departments[0].id,
            hire_date=date(2020, 3, 15),
            sick_leave_total=12,
            sick_leave_used=4,
            vacation_leave_total=18,
            vacation_leave_used=8,
            maternity_leave_total=90,
            maternity_leave_used=45,
        ),
        Employee(
            first_name="Liam",
            last_name="Garcia",
            email="liam.garcia@example.com",
            role="People Ops Specialist",
            gender="male",
            password="password123",
            department_id=departments[0].id,
            hire_date=date(2022, 7, 1),
            sick_leave_total=10,
            sick_leave_used=2,
            vacation_leave_total=15,
            vacation_leave_used=5,
        ),
        Employee(
            first_name="Maya",
            last_name="Chen",
            email="maya.chen@example.com",
            role="Senior Engineer",
            gender="female",
            password="password123",
            department_id=departments[1].id,
            hire_date=date(2019, 11, 4),
            sick_leave_total=14,
            sick_leave_used=6,
            vacation_leave_total=20,
            vacation_leave_used=12,
            maternity_leave_total=90,
            maternity_leave_used=0,
        ),
        Employee(
            first_name="Ethan",
            last_name="Brooks",
            email="ethan.brooks@example.com",
            role="Staff Engineer",
            gender="male",
            password="password123",
            department_id=departments[1].id,
            hire_date=date(2018, 5, 22),
            sick_leave_total=12,
            sick_leave_used=1,
            vacation_leave_total=18,
            vacation_leave_used=7,
        ),
        Employee(
            first_name="Noah",
            last_name="Patel",
            email="noah.patel@example.com",
            role="Account Executive",
            gender="male",
            password="password123",
            department_id=departments[2].id,
            hire_date=date(2021, 2, 9),
            sick_leave_total=10,
            sick_leave_used=3,
            vacation_leave_total=15,
            vacation_leave_used=6,
        ),
        Employee(
            first_name="Zoe",
            last_name="Kim",
            email="zoe.kim@example.com",
            role="Finance Analyst",
            gender="female",
            password="password123",
            department_id=departments[3].id,
            hire_date=date(2023, 1, 16),
            sick_leave_total=12,
            sick_leave_used=0,
            vacation_leave_total=15,
            vacation_leave_used=2,
            maternity_leave_total=90,
            maternity_leave_used=0,
        ),
    ]
    db.session.add_all(employees)
    db.session.flush()

    now = datetime.utcnow()
    attendance_entries = [
        AttendanceRecord(
            employee_id=employees[0].id,
            check_in=now - timedelta(days=3, hours=9),
            check_out=now - timedelta(days=3, hours=1),
        ),
        AttendanceRecord(
            employee_id=employees[0].id,
            check_in=now - timedelta(days=1, hours=4),
            check_out=now - timedelta(days=1, hours=1),
        ),
        AttendanceRecord(
            employee_id=employees[1].id,
            check_in=now - timedelta(days=2, hours=5),
            check_out=now - timedelta(days=2),
        ),
        AttendanceRecord(
            employee_id=employees[1].id,
            check_in=now - timedelta(hours=6),
        ),
        AttendanceRecord(
            employee_id=employees[2].id,
            check_in=now - timedelta(days=1, hours=2),
            check_out=now - timedelta(days=1),
        ),
        AttendanceRecord(
            employee_id=employees[2].id,
            check_in=now - timedelta(hours=3),
        ),
        AttendanceRecord(
            employee_id=employees[3].id,
            check_in=now - timedelta(days=4, hours=9),
            check_out=now - timedelta(days=4, hours=2),
        ),
        AttendanceRecord(
            employee_id=employees[4].id,
            check_in=now - timedelta(days=2, hours=8),
            check_out=now - timedelta(days=2, hours=1),
        ),
        AttendanceRecord(
            employee_id=employees[5].id,
            check_in=now - timedelta(days=1, hours=7),
            check_out=now - timedelta(days=1, hours=2),
        ),
    ]
    db.session.add_all(attendance_entries)

    leave_requests = [
        LeaveRequest(
            employee_id=employees[0].id,
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=12),
            reason="Family trip",
            status="pending",
        ),
        LeaveRequest(
            employee_id=employees[2].id,
            start_date=date.today() - timedelta(days=3),
            end_date=date.today() - timedelta(days=1),
            reason="Medical leave",
            status="approved",
        ),
        LeaveRequest(
            employee_id=employees[5].id,
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=40),
            reason="Maternity leave",
            status="approved",
        ),
    ]
    db.session.add_all(leave_requests)
    db.session.commit()

