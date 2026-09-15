from flask import Flask, jsonify,request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# ============================================
# HOME
# ============================================

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "SmartReassign AI Backend is running!",
        "status": "online"
    })


# ============================================
# EMPLOYEES
# ============================================

@app.route("/employees", methods=["GET"])
def get_employees():

    employees = [
        {
            "employee_id": "E001",
            "name": "Arun",
            "department": "Warehouse",
            "role": "Picker",
            "skills": ["Picking", "Inventory"],
            "performance": 92,
            "workload": 30,
            "availability": "Available"
        },
        {
            "employee_id": "E002",
            "name": "Priya",
            "department": "Warehouse",
            "role": "Packing Operator",
            "skills": ["Packing", "Quality Check"],
            "performance": 88,
            "workload": 70,
            "availability": "Available"
        },
        {
            "employee_id": "E003",
            "name": "Kavin",
            "department": "Warehouse",
            "role": "Packing Operator",
            "skills": ["Packing", "Inventory"],
            "performance": 95,
            "workload": 25,
            "availability": "Available"
        },
        {
            "employee_id": "E004",
            "name": "Divya",
            "department": "Warehouse",
            "role": "Picker",
            "skills": ["Picking", "Sorting"],
            "performance": 85,
            "workload": 50,
            "availability": "Available"
        },
        {
            "employee_id": "E005",
            "name": "Ravi",
            "department": "Warehouse",
            "role": "Sorting Operator",
            "skills": ["Sorting", "Inventory"],
            "performance": 90,
            "workload": 20,
            "availability": "Available"
        }
    ]

    return jsonify({
        "success": True,
        "count": len(employees),
        "employees": employees
    })


# ============================================
# ROLES & SKILLS
# ============================================

@app.route("/roles", methods=["GET"])
def get_roles():

    roles = [
        {
            "role_id": "R001",
            "role": "Picker",
            "department": "Warehouse",
            "required_skills": ["Picking", "Inventory"]
        },
        {
            "role_id": "R002",
            "role": "Packing Operator",
            "department": "Warehouse",
            "required_skills": ["Packing", "Quality Check"]
        },
        {
            "role_id": "R003",
            "role": "Sorting Operator",
            "department": "Warehouse",
            "required_skills": ["Sorting", "Inventory"]
        },
        {
            "role_id": "R004",
            "role": "Quality Inspector",
            "department": "Warehouse",
            "required_skills": ["Quality Check", "Inspection"]
        },
        {
            "role_id": "R005",
            "role": "Inventory Coordinator",
            "department": "Warehouse",
            "required_skills": ["Inventory", "Stock Management"]
        }
    ]

    return jsonify({
        "success": True,
        "count": len(roles),
        "roles": roles
    })


# ============================================
# MONTHLY SCHEDULE
# ============================================

@app.route("/schedule", methods=["GET"])
def get_schedule():

    schedule = [
        {
            "date": "2026-09-01",
            "employee_id": "E001",
            "employee": "Arun",
            "shift": "Morning",
            "role": "Picker",
            "task": "Order Picking Zone A",
            "status": "Scheduled"
        },
        {
            "date": "2026-09-01",
            "employee_id": "E002",
            "employee": "Priya",
            "shift": "Morning",
            "role": "Packing Operator",
            "task": "Product Packing Zone B",
            "status": "Scheduled"
        },
        {
            "date": "2026-09-01",
            "employee_id": "E003",
            "employee": "Kavin",
            "shift": "Morning",
            "role": "Packing Operator",
            "task": "Product Packing Zone A",
            "status": "Scheduled"
        },
        {
            "date": "2026-09-01",
            "employee_id": "E004",
            "employee": "Divya",
            "shift": "Morning",
            "role": "Picker",
            "task": "Order Picking Zone C",
            "status": "Scheduled"
        },
        {
            "date": "2026-09-01",
            "employee_id": "E005",
            "employee": "Ravi",
            "shift": "Morning",
            "role": "Sorting Operator",
            "task": "Inventory Sorting",
            "status": "Scheduled"
        }
    ]

    return jsonify({
        "success": True,
        "month": "September",
        "year": 2026,
        "schedule": schedule
    })
# ============================================
# LEAVE MANAGEMENT API
# ============================================

@app.route("/leave", methods=["POST"])
def apply_leave():

    data = request.get_json()

    employee_id = data.get("employee_id")
    leave_date = data.get("leave_date")
    leave_type = data.get("leave_type")
    reason = data.get("reason", "")

    if not employee_id or not leave_date or not leave_type:
        return jsonify({
            "success": False,
            "message": "employee_id, leave_date and leave_type are required"
        }), 400

    if leave_type not in ["Planned", "Emergency"]:
        return jsonify({
            "success": False,
            "message": "leave_type must be Planned or Emergency"
        }), 400

    leave = {
        "leave_id": "L001",
        "employee_id": employee_id,
        "leave_date": leave_date,
        "leave_type": leave_type,
        "reason": reason,
        "status": "Pending"
    }

    return jsonify({
        "success": True,
        "message": "Leave request submitted successfully.",
        "leave": leave
    })


# ============================================
# LEAVE APPROVAL API
# ============================================

@app.route("/leave/approve", methods=["POST"])
def approve_leave():

    data = request.get_json()

    employee_id = data.get("employee_id")
    leave_date = data.get("leave_date")

    if not employee_id or not leave_date:
        return jsonify({
            "success": False,
            "message": "employee_id and leave_date are required"
        }), 400

    return jsonify({
        "success": True,
        "employee_id": employee_id,
        "leave_date": leave_date,
        "status": "Approved",
        "message": "Leave approved. AI reassignment planning initiated."
    })
    # ============================================
# AI REASSIGNMENT - MULTIPLE CANDIDATES
# ============================================

@app.route("/ai-reassign", methods=["POST"])
def ai_reassign():

    data = request.get_json()

    absent_employee_id = data.get("employee_id")
    task_type = data.get("task_type")
    task_name = data.get("task_name", "Unassigned Task")

    if not absent_employee_id or not task_type:
        return jsonify({
            "success": False,
            "message": "employee_id and task_type are required"
        }), 400

    # Company employees
    employees = [
        {
            "employee_id": "E001",
            "name": "Arun",
            "skills": ["Picking", "Inventory"],
            "performance": 92,
            "workload": 30,
            "availability": "Available"
        },
        {
            "employee_id": "E002",
            "name": "Priya",
            "skills": ["Packing", "Quality Check"],
            "performance": 88,
            "workload": 70,
            "availability": "Available"
        },
        {
            "employee_id": "E003",
            "name": "Kavin",
            "skills": ["Packing", "Inventory"],
            "performance": 95,
            "workload": 25,
            "availability": "Available"
        },
        {
            "employee_id": "E004",
            "name": "Divya",
            "skills": ["Picking", "Sorting"],
            "performance": 85,
            "workload": 50,
            "availability": "Available"
        },
        {
            "employee_id": "E005",
            "name": "Ravi",
            "skills": ["Sorting", "Inventory"],
            "performance": 90,
            "workload": 20,
            "availability": "Available"
        }
    ]

    candidates = []

    for employee in employees:

        # Don't select the absent employee
        if employee["employee_id"] == absent_employee_id:
            continue

        # Don't select unavailable employees
        if employee["availability"] != "Available":
            continue

        # Don't overload employees
        if employee["workload"] >= 80:
            continue

        # ----------------------------------------
        # SKILL MATCH
        # ----------------------------------------

        if task_type in employee["skills"]:
            skill_score = 100
        else:
            skill_score = 30

        # ----------------------------------------
        # WORKLOAD SCORE
        # Lower workload = better
        # ----------------------------------------

        workload_score = 100 - employee["workload"]

        # ----------------------------------------
        # FINAL AI SUITABILITY SCORE
        # ----------------------------------------

        ai_score = (
            skill_score * 0.45
            + employee["performance"] * 0.35
            + workload_score * 0.20
        )

        expected_workload = employee["workload"] + 20

        if expected_workload <= 50:
            risk = "LOW"
        elif expected_workload <= 70:
            risk = "MEDIUM"
        else:
            risk = "HIGH"

        candidates.append({
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "skills": employee["skills"],
            "skill_score": skill_score,
            "performance": employee["performance"],
            "current_workload": employee["workload"],
            "expected_workload": expected_workload,
            "ai_score": round(ai_score, 2),
            "ripple_risk": risk
        })

    # ----------------------------------------
    # RANK CANDIDATES
    # ----------------------------------------

    candidates.sort(
        key=lambda x: x["ai_score"],
        reverse=True
    )

    if not candidates:
        return jsonify({
            "success": False,
            "message": "No suitable replacement found."
        }), 404

    best_candidate = candidates[0]

    return jsonify({
        "success": True,

        "task": {
            "task_name": task_name,
            "task_type": task_type,
            "absent_employee": absent_employee_id
        },

        "recommended_employee": best_candidate,

        "candidate_ranking": candidates,

        "explanation": {
            "skill": "Skill compatibility considered",
            "performance": "Historical performance considered",
            "workload": "Current workload considered",
            "risk": "Expected workload and ripple risk considered"
        }
    })
# ============================================
# APPROVE AI REASSIGNMENT
# ============================================

@app.route("/approve-reassignment", methods=["POST"])
def approve_reassignment():

    data = request.get_json()

    absent_employee = data.get("absent_employee")
    replacement_employee = data.get("replacement_employee")
    task_name = data.get("task_name")

    if not absent_employee or not replacement_employee or not task_name:
        return jsonify({
            "success": False,
            "message": "absent_employee, replacement_employee and task_name are required"
        }), 400

    # Demo workload data
    workloads = {
        "E001": 30,
        "E002": 70,
        "E003": 25,
        "E004": 50,
        "E005": 20
    }

    names = {
        "E001": "Arun",
        "E002": "Priya",
        "E003": "Kavin",
        "E004": "Divya",
        "E005": "Ravi"
    }

    if replacement_employee not in workloads:
        return jsonify({
            "success": False,
            "message": "Replacement employee not found."
        }), 404

    old_workload = workloads[replacement_employee]

    # Add reassigned task workload
    new_workload = old_workload + 20

    if new_workload > 100:
        return jsonify({
            "success": False,
            "message": "Replacement employee would become overloaded."
        }), 400

    workloads[replacement_employee] = new_workload

    return jsonify({
        "success": True,

        "message": "Task successfully reassigned.",

        "reassignment": {
            "task": task_name,
            "from_employee": absent_employee,
            "to_employee": replacement_employee,
            "replacement_name": names[replacement_employee],
            "previous_workload": old_workload,
            "updated_workload": new_workload,
            "status": "Reassigned"
        }
    })



# ============================================
# START SERVER
# ============================================

if __name__ == "__main__":

    print("====================================")
    print("SMART REASSIGN AI BACKEND")
    print("====================================")
    print("Server starting...")
    print("URL: http://127.0.0.1:5000")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )