async function analyzeAbsence(employeeId) {

    const resultSection = document.getElementById("result");

    resultSection.classList.remove("hidden");

    document.getElementById("bestName").innerText = "Analyzing...";
    document.getElementById("bestId").innerText = "";
    document.getElementById("bestScore").innerText = "";

    try {

        const response = await fetch(
            "https://smart-reassign-ai.onrender.com/reassign",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    employee_id: employeeId
                })
            }
        );

        const data = await response.json();

        if (!data.success) {
            alert(data.message);
            return;
        }

        // Absent employee details
        document.getElementById("absent").innerText =
            data.absent_employee;

        document.getElementById("task").innerText =
            data.task.task_name;

        document.getElementById("taskType").innerText =
            data.task.task_type;


        // Best replacement
        const best = data.best_replacement;

        document.getElementById("bestName").innerText =
            best.name;

        document.getElementById("bestId").innerText =
            best.employee_id;

        document.getElementById("bestScore").innerText =
            best.score;


        // What-If Workload Impact
        const whatIfBox = document.querySelector(".whatif-box");

        const riskClass =
            best.ripple_risk.toLowerCase() === "low"
                ? "low-risk"
                : "medium-risk";

        whatIfBox.innerHTML = `
            <h3>🔮 What-If Workload Impact</h3>

            <p>
                AI predicts the workload impact before reassignment.
            </p>

            <div class="impact-row">

                <div>
                    <strong>
                        ${best.name} (${best.employee_id})
                    </strong>

                    <span class="${riskClass}">
                        ${best.ripple_risk.toUpperCase()} RISK
                    </span>
                </div>

                <p>
                    Current Workload:
                    ${best.current_workload}%
                </p>

                <p>
                    After Reassignment:
                    <strong>${best.after_workload}%</strong>
                </p>

                <p>
                    Ripple Effect:
                    <strong>${best.ripple_risk}</strong>
                </p>

            </div>

            <div class="recommendation">

                🏆 <strong>AI Recommendation:</strong>

                ${best.name} provides the lowest
                operational disruption.

            </div>
        `;


        // Candidate Ranking
        const ranking =
            document.getElementById("ranking");

        ranking.innerHTML = "";


        data.candidate_rankings.forEach(candidate => {

            const row =
                document.createElement("tr");

            row.innerHTML = `
                <td>
                    ${candidate.name}
                    (${candidate.employee_id})
                </td>

                <td>
                    ${candidate.skill}
                </td>

                <td>
                    ${candidate.performance}
                </td>

                <td>
                    ${candidate.workload}%
                </td>

                <td>
                    <strong>
                        ${candidate.score}
                    </strong>
                </td>
            `;

            ranking.appendChild(row);

        });

    }

    catch (error) {

        console.error(error);

        alert(
            "Cannot connect to SmartReassign AI backend. " +
            "Make sure Flask server is running."
        );

    }

}


// Manager Approval
function approveReassignment() {

    const message =
        document.getElementById("approvalMessage");

    message.innerText =
        "✅ Task T002 successfully reassigned to Kavin (E003).";

    message.style.color = "green";

    message.style.fontWeight = "bold";

}


// Biometric Simulation
function simulateBiometric() {

    const scanStatus =
        document.getElementById("scanStatus");

    const scanEmployee =
        document.getElementById("scanEmployee");

    const scanResult =
        document.getElementById("scanResult");


    scanStatus.classList.remove("hidden");

    scanEmployee.innerText =
        "E002 - Priya";

    scanResult.innerText =
        "ABSENT";

}