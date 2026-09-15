var currentAbsentEmployee = null;
var currentReplacementEmployee = null;
var currentTaskName = null;


// =============================================
// BIOMETRIC SIMULATION
// =============================================

function simulateBiometric() {

    var scanStatus = document.getElementById("scanStatus");
    var scanEmployee = document.getElementById("scanEmployee");
    var scanResult = document.getElementById("scanResult");

    scanStatus.classList.remove("hidden");

    currentAbsentEmployee = "E002";

    scanEmployee.innerText = "E002 - Priya";
    scanResult.innerText = "ABSENT";
}


// =============================================
// AI REASSIGNMENT
// =============================================

function analyzeAbsence(employeeId) {

    currentAbsentEmployee = employeeId;

    fetch("http://127.0.0.1:5000/ai-reassign", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            employee_id: employeeId,
            task_type: "Packing",
            task_name: "Product Packing Zone B"
        })

    })

    .then(function(response) {

        return response.json();

    })

    .then(function(data) {

        console.log("AI RESPONSE:", data);

        if (!data.success) {

            alert(data.message || "AI analysis failed");

            return;
        }


        // =====================================
        // SHOW RESULT SECTION
        // =====================================

        document
            .getElementById("result")
            .classList.remove("hidden");


        // =====================================
        // TASK DETAILS
        // =====================================

        document.getElementById("absent").innerText =
            data.task.absent_employee;

        document.getElementById("task").innerText =
            data.task.task_name;

        document.getElementById("taskType").innerText =
            data.task.task_type;


        currentTaskName =
            data.task.task_name;


        // =====================================
        // BEST REPLACEMENT
        // =====================================

        currentReplacementEmployee =
            data.recommended_employee.employee_id;


        document.getElementById("bestName").innerText =
            data.recommended_employee.name;

        document.getElementById("bestId").innerText =
            data.recommended_employee.employee_id;

        document.getElementById("bestScore").innerText =
            data.recommended_employee.ai_score + "%";


        // =====================================
        // WHAT-IF WORKLOAD
        // =====================================

        document.querySelector(".whatif-box").innerHTML =

            "<h3>🔮 What-If Workload Impact</h3>" +

            "<p>" +
            "AI predicts the workload impact before reassignment." +
            "</p>" +

            "<div class='impact-row'>" +

            "<div>" +

            "<strong>Predicted Workload:</strong> " +

            data.recommended_employee.current_workload +

            "% → " +

            data.recommended_employee.expected_workload +

            "%" +

            "<br><br>" +

            "<strong>Ripple Risk:</strong> " +

            (data.recommended_employee.risk || "LOW") +

            "</div>" +

            "</div>";


        // =====================================
        // CANDIDATE RANKING
        // =====================================

        var ranking =
            document.getElementById("ranking");

        ranking.innerHTML = "";


        data.candidate_ranking.forEach(
            function(candidate, index) {

                var row =
                    document.createElement("tr");


                row.innerHTML =

                    "<td>" +
                    (index + 1) +
                    "</td>" +

                    "<td>" +
                    candidate.name +
                    " (" +
                    candidate.employee_id +
                    ")" +
                    "</td>" +

                    "<td>" +
                    candidate.skills.join(", ") +
                    "</td>" +

                    "<td>" +
                    candidate.performance +
                    "%" +
                    "</td>" +

                    "<td>" +
                    candidate.current_workload +
                    "%" +
                    "</td>" +

                    "<td>" +
                    candidate.ai_score +
                    "%" +
                    "</td>" +

                    "<td>" +
                    (candidate.risk || "LOW") +
                    "</td>";


                ranking.appendChild(row);

            }
        );

    })

    .catch(function(error) {

        console.error(
            "AI ERROR:",
            error
        );

        alert(
            "Cannot connect to SmartReassign AI backend."
        );

    });
}


// =============================================
// MANAGER APPROVAL
// =============================================

async function approveReassignment() {

    var message =
        document.getElementById("approvalMessage");


    message.innerText =
        "Processing approval...";

    message.style.color =
        "orange";


    try {

        var response = await fetch(

            "http://127.0.0.1:5000/approve-reassignment",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    absent_employee:
                        currentAbsentEmployee,

                    replacement_employee:
                        currentReplacementEmployee,

                    task_name:
                        currentTaskName

                })

            }

        );


        var data =
            await response.json();


        if (!data.success) {

            message.innerText =
                "❌ " +
                data.message;

            message.style.color =
                "red";

            return;

        }


        var r =
            data.reassignment;


        message.innerHTML =

            "✅ <strong>" +
            "Task Successfully Reassigned!" +
            "</strong><br><br>" +

            "Task: " +
            r.task +
            "<br>" +

            "From: " +
            r.from_employee +
            "<br>" +

            "To: " +
            r.replacement_name +
            " (" +
            r.to_employee +
            ")<br>" +

            "Workload: " +
            r.previous_workload +
            "% → " +
            r.updated_workload +
            "%<br>" +

            "Status: " +
            r.status;


        message.style.color =
            "green";

        message.style.fontWeight =
            "bold";

    }

    catch (error) {

        console.error(error);

        message.innerText =
            "❌ Cannot connect to backend.";

        message.style.color =
            "red";

    }
}


console.log(
    "SmartReassign JavaScript loaded"
);