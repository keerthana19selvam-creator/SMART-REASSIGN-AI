import sqlite3

DB_NAME = "smartreassign.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Employees
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT,
            role TEXT,
            skills TEXT,
            performance_score REAL,
            avg_completion_time REAL,
            error_rate REAL,
            current_workload REAL,
            availability TEXT DEFAULT 'Yes'
        )
    """)

    # Tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            task_name TEXT NOT NULL,
            task_type TEXT,
            assigned_employee TEXT,
            priority TEXT,
            estimated_time REAL,
            status TEXT
        )
    """)

    # Monthly Schedule
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            date TEXT,
            shift TEXT,
            role TEXT,
            task_id TEXT,
            status TEXT
        )
    """)

    # Leave Requests
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaves (
            leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            leave_date TEXT,
            leave_type TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)

    # Attendance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            date TEXT,
            shift TEXT,
            attendance_status TEXT,
            source TEXT
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()