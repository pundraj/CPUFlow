# 🖥️ Interactive OS CPU Scheduling Algorithm Visualizer

A **production-ready full-stack web application** that simulates and visually demonstrates how different CPU scheduling algorithms work, featuring real-time execution visualization, performance metrics, and algorithm comparison.

![Tech Stack](https://img.shields.io/badge/React-18-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green) ![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-cyan) ![Python](https://img.shields.io/badge/Python-3.10+-yellow)

---

## 🎯 Features

### Supported Algorithms
| Algorithm | Type | Key |
|-----------|------|-----|
| First Come First Serve (FCFS) | Non-Preemptive | `fcfs` |
| Shortest Job First (SJF) | Non-Preemptive | `sjf` |
| Shortest Remaining Time First (SRTF) | Preemptive | `srtf` |
| Priority Scheduling (Non-Preemptive) | Non-Preemptive | `priority_np` |
| Priority Scheduling (Preemptive) | Preemptive | `priority_p` |
| Round Robin (configurable quantum) | Preemptive | `round_robin` |
| Multilevel Queue Scheduling | Preemptive | `multilevel_queue` |
| Multilevel Feedback Queue (MLFQ) | Preemptive | `mlfq` |

### Visualization
- **Animated Gantt Chart** with color-coded processes
- **Step-by-step simulation** with Play/Pause/Stop controls
- **Speed control** (Slow / Medium / Fast)
- **Process state transitions** (Not Arrived → Ready → Running → Completed)
- **Dark / Light mode** toggle

### Analysis
- Per-process metrics (CT, TAT, WT, RT)
- Summary metrics (Avg WT, Avg TAT, CPU Utilization, Throughput)
- **Algorithm comparison mode** – run all 8 algorithms on the same input
- **Fairness analysis** with coefficient of variation
- **Bar charts** comparing algorithms side by side

### Additional
- Random process generator
- CSV export (single result or comparison)
- Time complexity info for each algorithm
- Responsive layout (mobile-friendly)
- Proper error handling (edge cases: idle time, zero burst, same arrivals)

---

## 🏗️ Project Structure

```
Scheduling project/
├── backend/
│   ├── app/
│   │   ├── algorithms/          # Each algorithm in its own file
│   │   │   ├── fcfs.py
│   │   │   ├── sjf.py
│   │   │   ├── srtf.py
│   │   │   ├── priority.py
│   │   │   ├── round_robin.py
│   │   │   ├── multilevel_queue.py
│   │   │   └── mlfq.py
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   ├── routes/
│   │   │   └── scheduling.py    # API endpoints
│   │   ├── services/
│   │   │   ├── scheduler_service.py  # Algorithm orchestration
│   │   │   └── export_service.py     # CSV export logic
│   │   └── main.py              # FastAPI app entry point
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── ProcessInput.jsx
│   │   │   ├── GanttChart.jsx
│   │   │   ├── SimulationControls.jsx
│   │   │   ├── MetricsTable.jsx
│   │   │   ├── ComparisonChart.jsx
│   │   │   ├── ProcessStateTimeline.jsx
│   │   │   └── AlgorithmInfo.jsx
│   │   ├── pages/
│   │   │   └── Dashboard.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   │   ├── useDarkMode.js
│   │   │   └── useSimulation.js
│   │   ├── utils/
│   │   │   └── helpers.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** (with npm)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd "Scheduling project"
```

### 2. Backend Setup

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.  
Swagger docs: `http://localhost:8000/docs`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/schedule` | Run a single algorithm |
| `POST` | `/api/compare` | Compare multiple algorithms |
| `GET`  | `/api/algorithms` | List algorithm metadata |
| `POST` | `/api/export/csv` | Export single result as CSV |
| `POST` | `/api/export/compare` | Export comparison as CSV |
| `GET`  | `/health` | Health check |

### Example Request

```json
POST /api/schedule
{
  "processes": [
    { "pid": "P1", "arrival_time": 0, "burst_time": 5, "priority": 2 },
    { "pid": "P2", "arrival_time": 1, "burst_time": 3, "priority": 1 },
    { "pid": "P3", "arrival_time": 2, "burst_time": 8, "priority": 3 }
  ],
  "algorithm": "round_robin",
  "time_quantum": 3
}
```

### Example Response

```json
{
  "algorithm": "Round Robin (RR)",
  "gantt_chart": [
    { "process": "P1", "start": 0, "end": 3 },
    { "process": "P2", "start": 3, "end": 6 },
    { "process": "P3", "start": 6, "end": 9 },
    { "process": "P1", "start": 9, "end": 11 },
    { "process": "P3", "start": 11, "end": 16 }
  ],
  "metrics": {
    "completion_times": { "P1": 11, "P2": 6, "P3": 16 },
    "turnaround_times": { "P1": 11, "P2": 5, "P3": 14 },
    "waiting_times": { "P1": 6, "P2": 2, "P3": 6 },
    "response_times": { "P1": 0, "P2": 2, "P3": 4 },
    "average_waiting_time": 4.67,
    "average_turnaround_time": 10.0,
    "cpu_utilization": 100.0,
    "throughput": 0.1875
  }
}
```

---

## 🌐 Deployment Guide

### Backend (e.g., Railway, Render, or any VPS)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Set the `PORT` env variable if required by the platform.

### Frontend (e.g., Vercel, Netlify)

```bash
cd frontend
npm run build
# Output in dist/ – deploy this folder as a static site
```

Set the environment variable `VITE_API_URL` to your deployed backend URL before building:

```bash
VITE_API_URL=https://your-backend.example.com npm run build
```

---

## 🧪 Edge Cases Handled

- **CPU idle time**: Idle blocks are shown in the Gantt chart
- **Same arrival times**: Tie-breaking by burst time / priority / PID
- **Same priorities**: Tie-breaking by arrival time, then PID
- **Zero burst time**: Processes are immediately completed
- **Large inputs**: Algorithms handle 100+ processes efficiently

---

## 📄 License

MIT License – free to use, modify, and distribute.
