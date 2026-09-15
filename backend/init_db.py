from database import get_db


def init_database():

    conn = get_db()
    cursor = conn.cursor()

    # Company
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Employees
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT,
            role TEXT,
            performance_score REAL DEFAULT 0,
            current_workload REAL DEFAULT 0,
            availability TEXT DEFAULT 'Available',
            company_id INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Roles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role_code TEXT,
            role_name TEXT NOT NULL,
            company_id INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Skills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            company_id INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Employee Skills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            skill_id INTEGER NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (skill_id) REFERENCES skills(id)
        )
    """)

    # Tasks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT UNIQUE NOT NULL,
            task_name TEXT NOT NULL,
            task_type TEXT,
            assigned_employee TEXT,
            priority TEXT,
            estimated_time REAL,
            status TEXT,
            company_id INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Schedule
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            schedule_date TEXT NOT NULL,
            shift TEXT,
            role TEXT,
            task_id TEXT,
            company_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (task_id) REFERENCES tasks(task_id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Attendance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            attendance_date TEXT NOT NULL,
            shift TEXT,
            check_in TEXT,
            check_out TEXT,
            attendance_status TEXT,
            source TEXT,
            company_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    # Leave
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            leave_date TEXT NOT NULL,
            leave_type TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Pending',
            company_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY (company_id) REFERENCES companies(id)
        )
    """)

    conn.commit()
    conn.close()

    print("SmartReassign AI database initialized successfully!")


if __name__ == "__main__":
    init_database()