import sqlite3
import pandas as pd

DB_NAME = "smartreassign.db"


def seed_database():

    conn = sqlite3.connect(DB_NAME)

    # -----------------------------
    # EMPLOYEES
    # -----------------------------
    employees = pd.read_csv("data/employees.csv")

    employees = employees.rename(columns={
        "id": "employee_id"
    })

    # Add missing columns if needed
    required_employee_columns = [
        "employee_id",
        "name",
        "department",
        "primary_skill",
        "performance_score",
        "avg_completion_time",
        "error_rate",
        "current_workload",
        "availability"
    ]

    for col in required_employee_columns:
        if col not in employees.columns:
            employees[col] = ""

    employees = employees[required_employee_columns]

    # role + skills
    employees["role"] = employees["primary_skill"]
    employees["skills"] = employees["primary_skill"]

    employees.to_sql(
        "employees",
        conn,
        if_exists="replace",
        index=False
    )

    # -----------------------------
    # TASKS
    # -----------------------------
    tasks = pd.read_csv("data/tasks.csv")

    tasks = tasks.rename(columns={
        "assigned_employee": "assigned_employee"
    })

    tasks.to_sql(
        "tasks",
        conn,
        if_exists="replace",
        index=False
    )

    # -----------------------------
    # ATTENDANCE
    # -----------------------------
    attendance = pd.read_csv("data/attendance.csv")

    attendance.to_sql(
        "attendance",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("================================")
    print("DATABASE SEEDED SUCCESSFULLY!")
    print("================================")
    print("Employees :", len(employees))
    print("Tasks     :", len(tasks))
    print("Attendance:", len(attendance))


if __name__ == "__main__":
    seed_database()