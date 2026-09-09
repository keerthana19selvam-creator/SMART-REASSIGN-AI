import os
import pandas as pd

# Project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load datasets
employees = pd.read_csv(
    os.path.join(BASE_DIR, "data", "employees.csv")
)

tasks = pd.read_csv(
    os.path.join(BASE_DIR, "data", "tasks.csv")
)


def calculate_suitability(employee, task_type):

    # 1. Skill match
    if employee["primary_skill"] == task_type:
        skill_score = 100
    else:
        skill_score = 40

    # 2. Performance
    performance_score = employee["performance_score"]

    # 3. Error rate
    error_score = max(0, 100 - employee["error_rate"] * 10)

    # 4. Lower workload = better
    workload_score = 100 - employee["current_workload"]

    # 5. Availability
    availability_score = (
        100 if employee["availability"] == "Yes" else 0
    )

    # Final AI suitability score
    final_score = (
        skill_score * 0.30
        + performance_score * 0.25
        + error_score * 0.15
        + workload_score * 0.20
        + availability_score * 0.10
    )

    return round(final_score, 2)


def find_best_replacement(absent_employee_id):

    # Find tasks assigned to absent employee
    absent_tasks = tasks[
        tasks["assigned_employee"] == absent_employee_id
    ]

    if absent_tasks.empty:
        return None

    task = absent_tasks.iloc[0]
    task_type = task["task_type"]

    # Candidates
    candidates = employees[
        (employees["employee_id"] != absent_employee_id)
        & (employees["availability"] == "Yes")
        & (employees["current_workload"] < 80)
    ].copy()

    # Calculate scores
    candidates["suitability_score"] = candidates.apply(
        lambda employee: calculate_suitability(
            employee,
            task_type
        ),
        axis=1
    )

    # Rank candidates
    candidates = candidates.sort_values(
        by="suitability_score",
        ascending=False
    )

    return task, candidates


# Demo
if __name__ == "__main__":

    absent_employee = "E002"

    result = find_best_replacement(absent_employee)

    if result is None:
        print("No task found for absent employee.")
    else:
        task, candidates = result

        print("\n===================================")
        print("     SMART REASSIGN AI")
        print("===================================")

        print(f"\nAbsent Employee: {absent_employee}")
        print(f"Task: {task['task_name']}")
        print(f"Task Type: {task['task_type']}")

        print("\nCandidate Ranking:")
        print("-----------------------------------")

        for _, employee in candidates.iterrows():

            print(
                f"{employee['name']} "
                f"({employee['employee_id']}) "
                f"-> Score: "
                f"{employee['suitability_score']}"
            )

        best = candidates.iloc[0]

        print("\n===================================")
        print("BEST REPLACEMENT")
        print("===================================")

        print(f"Employee: {best['name']}")
        print(f"Employee ID: {best['employee_id']}")
        print(f"Suitability Score: {best['suitability_score']}")

        print("\nReason:")
        print("- Skill match")
        print("- Good performance")
        print("- Low error rate")
        print("- Available workload")