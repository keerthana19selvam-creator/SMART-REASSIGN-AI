# SmartReassign AI

## AI-Powered Sudden Absence Task Reassignment System

SmartReassign AI is an intelligent workforce management system that automatically identifies tasks affected by employee absence and recommends the most suitable replacement.

Unlike traditional systems that select replacements only based on skill availability, SmartReassign AI also predicts the **workload ripple effect** caused by reassignment and recommends the candidate that minimizes operational disruption.

## Problem Statement

When an employee suddenly becomes absent, managers often manually decide who should take over their tasks.

This can cause:

* Delayed task reassignment
* Incorrect employee selection
* Workload imbalance
* Increased operational risk
* Dependency on manual decisions

## Solution

SmartReassign AI automates the decision-making process.

### Workflow

Biometric Attendance Simulation
↓
Absence Detection
↓
Task Identification
↓
AI Candidate Ranking
↓
Workload Ripple Prediction
↓
Best Replacement Selection
↓
Manager Approval
↓
Task Reassignment

## Key Features

* Simulated biometric attendance monitoring
* Automatic absence detection
* Task-at-risk identification
* AI-based candidate suitability scoring
* Skill and performance analysis
* Current workload analysis
* Error-rate consideration
* Workload Ripple Effect prediction
* Candidate ranking
* Manager approval workflow

## Novelty

### Workload Ripple Effect

The system does not simply ask:

> "Who can perform this task?"

It also asks:

> "What happens to the candidate's workload after taking this task?"

The system estimates the candidate's workload after reassignment and classifies the operational risk as:

* Low
* Medium
* High

This helps minimize the domino effect of sudden employee absence.

## Example

If Priya (E002) is absent from a Packing task:

**Kavin (E003)**

* Packing skill match
* Performance: 95
* Current workload: 25%
* Predicted workload: 45%
* Ripple risk: Low
* AI score: 92.25

The system therefore recommends Kavin as the best replacement.

## Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* Flask
* Flask-CORS

### Data & AI

* Python
* Pandas
* Rule-based AI scoring
* Workload impact prediction

## Project Structure

```text
SMART REASSIGN AI
│
├── backend
│   └── app.py
│
├── frontend
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data
│   ├── employees.csv
│   ├── tasks.csv
│   └── attendance.csv
│
├── ml
│   └── reassign_engine.py
│
└── README.md
```

## How to Run

### 1. Install dependencies

```bash
pip install flask flask-cors pandas
```

### 2. Start the backend

```bash
python backend/app.py
```

The backend will run at:

```text
http://127.0.0.1:5000
```

### 3. Open the frontend

Open:

```text
frontend/index.html
```

in a browser.

### 4. Demo

Click:

**Simulate Biometric Scan**

Then:

**Analyze & Reassign**

The system will rank available employees and recommend the lowest-disruption replacement.

## Future Enhancements

* Real biometric attendance integration
* Machine-learning-based performance prediction
* Real-time workforce monitoring
* Multi-task reassignment optimization
* Live notifications
* Enterprise HR system integration
* Advanced workload forecasting

## Impact

SmartReassign AI helps organizations respond to sudden workforce shortages quickly while reducing workload imbalance and operational disruption.

---

**SmartReassign AI — Intelligent workforce decisions when every second matters.**
