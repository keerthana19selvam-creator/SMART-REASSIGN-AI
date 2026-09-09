from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import pandas as pd

app = Flask(__name__)
CORS(app)

# ==================================================
# PROJECT ROOT
# ==================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ==================================================
# DATA FILE PATHS
# ==================================================

EMPLOYEES_FILE = os.path.join(
    BASE_DIR, "data", "employees.csv"
)

TASKS_FILE = os.path.join(
    BASE_DIR, "data", "tasks.csv"
)

ATTENDANCE_FILE = os.path.join(
    BASE_DIR, "data", "attendance.csv"
)


# ==================================================
# LOAD DATA
# ==================================================

def load_data():

    employees = pd.read_csv(EMPLOYEES_FILE)
    tasks = pd.read_csv(TASKS_FILE)
    attendance = pd.read_csv(ATTENDANCE_FILE)

    return employees, tasks, attendance


# ==================================================
# AI SUITABILITY SCORE
# ==================================================

def calculate_score(employee, task_type):

    # Skill match
    if employee["primary_skill"] == task_type:
        skill_score = 100
    else:
        skill_score = 40

    # Performance
    performance_score = employee["performance_score"]

    # Lower error rate = higher score
    error_score = max(
        0,
        100 - employee["error_rate"] * 10
    )

    # Lower workload = better
    workload_score = (
        100 - employee["current_workload"]
    )

    # Availability
    availability_score = (
        100
        if employee["availability"] == "Yes"
        else 0
    )

    # Weighted AI score
    score = (
        skill_score * 0.30
        + performance_score * 0.25
        + error_score * 0.15
        + workload_score * 0.20
        + availability_score * 0.10
    )

    return round(score, 2)


# ==================================================
# WORKLOAD RIPPLE EFFECT
# ==================================================

def calculate_ripple_risk(
    current_workload,
    task_time
):

    # Estimated workload increase
    workload_increase = task_time * 0.5

    after_workload = (
        current_workload
        + workload_increase
    )

    # Risk classification
    if after_workload <= 50:

        risk = "Low"

    elif after_workload <= 70:

        risk = "Medium"

    else:

        risk = "High"

    return round(after_workload, 1), risk


# ==================================================
# HOME API
# ==================================================

@app.route("/")
def home():

    return jsonify({

        "status": "online",

        "message":
        "SmartReassign AI Backend is running!"

    })


# ==================================================
# REASSIGN API
# ==================================================

@app.route(
    "/reassign",
    methods=["POST"]
)
def reassign():

    try:

        # ------------------------------------------
        # Get request data
        # ------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({

                "success": False,

                "message":
                "Request body is missing."

            }), 400

        absent_employee_id = data.get(
            "employee_id"
        )

        if not absent_employee_id:

            return jsonify({

                "success": False,

                "message":
                "Employee ID is required."

            }), 400


        # ------------------------------------------
        # Load CSV data
        # ------------------------------------------

        employees, tasks, attendance = load_data()


        # ------------------------------------------
        # Find absent employee's task
        # ------------------------------------------

        employee_tasks = tasks[
            tasks["assigned_employee"]
            == absent_employee_id
        ]


        if employee_tasks.empty:

            return jsonify({

                "success": False,

                "message":
                "No task found for this employee."

            }), 404


        # Get first task
        task = employee_tasks.iloc[0]

        task_type = task["task_type"]


        # ------------------------------------------
        # Find suitable candidates
        # ------------------------------------------

        candidates = employees[
            (employees["employee_id"]
             != absent_employee_id)

            &

            (employees["availability"]
             == "Yes")

            &

            (employees["current_workload"]
             < 80)
        ].copy()


        if candidates.empty:

            return jsonify({

                "success": False,

                "message":
                "No suitable replacement available."

            }), 404


        # ------------------------------------------
        # Calculate AI suitability scores
        # ------------------------------------------

        candidates[
            "suitability_score"
        ] = candidates.apply(

            lambda employee:
            calculate_score(
                employee,
                task_type
            ),

            axis=1
        )


        # ------------------------------------------
        # Rank candidates
        # ------------------------------------------

        candidates = candidates.sort_values(

            by="suitability_score",

            ascending=False
        )


        # Best candidate
        best = candidates.iloc[0]


        # ------------------------------------------
        # Candidate ranking
        # ------------------------------------------

        rankings = []


        for _, employee in candidates.iterrows():

            after_workload, ripple_risk = (
                calculate_ripple_risk(

                    employee["current_workload"],

                    task["estimated_time"]
                )
            )


            rankings.append({

                "employee_id":
                employee["employee_id"],

                "name":
                employee["name"],

                "skill":
                employee["primary_skill"],

                "performance":
                int(employee["performance_score"]),

                "workload":
                int(employee["current_workload"]),

                "after_workload":
                after_workload,

                "ripple_risk":
                ripple_risk,

                "error_rate":
                int(employee["error_rate"]),

                "score":
                float(employee["suitability_score"])
            })


        # ------------------------------------------
        # Best candidate workload prediction
        # ------------------------------------------

        best_after_workload, best_ripple_risk = (
            calculate_ripple_risk(

                best["current_workload"],

                task["estimated_time"]
            )
        )


        # ------------------------------------------
        # FINAL RESPONSE
        # ------------------------------------------

        return jsonify({

            "success": True,

            "absent_employee":
            absent_employee_id,


            "task": {

                "task_id":
                task["task_id"],

                "task_name":
                task["task_name"],

                "task_type":
                task["task_type"],

                "priority":
                task["priority"],

                "estimated_time":
                int(task["estimated_time"])
            },


            "best_replacement": {

                "employee_id":
                best["employee_id"],

                "name":
                best["name"],

                "score":
                float(
                    best["suitability_score"]
                ),

                "current_workload":
                int(
                    best["current_workload"]
                ),

                "after_workload":
                best_after_workload,

                "ripple_risk":
                best_ripple_risk
            },


            "candidate_rankings":
            rankings
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({

            "success": False,

            "message":
            "Internal server error.",

            "error":
            str(e)

        }), 500


# ==================================================
# START SERVER
# ==================================================

if __name__ == "__main__":

    print(
        "==================================="
    )

    print(
        "     SMART REASSIGN AI BACKEND"
    )

    print(
        "==================================="
    )

    print(
        "Server starting..."
    )

    print(
        "URL: http://127.0.0.1:5000"
    )

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True
    )