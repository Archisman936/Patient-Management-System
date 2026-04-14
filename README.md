# 🏥 Patient Management System

A personal full-stack web application for managing patient health records, built with **FastAPI** and **Streamlit**.

> This is a personal project built to explore and learn full-stack development with Python — combining a RESTful API backend with an interactive, modern frontend.

---

## ✨ Features

- **Dashboard** — Overview of total patients, average age, average BMI, and health verdicts at a glance
- **View All Patients** — Browse every record in card view and table view
- **Search** — Look up any patient instantly by their ID
- **Add Patient** — Register new patients with full health details
- **Update Patient** — Edit existing records with a pre-filled form
- **Delete Patient** — Remove records with a confirmation safeguard
- **Sort Patients** — Sort by height, weight, or BMI in ascending/descending order with a live bar chart
- **Auto BMI & Verdict** — BMI is calculated automatically; patients are classified as Underweight, Normal, Overweight, or Obese

---

## 🛠️ Tech Stack

| Layer       | Technology                |
| ----------- | ------------------------- |
| **Backend** | FastAPI, Pydantic, Uvicorn |
| **Frontend**| Streamlit, Pandas          |
| **Data**    | JSON (file-based storage)  |
| **DevOps**  | Docker                     |

---

## 📂 Project Structure

```
Patients_project/
├── Backend/
│   └── main.py            # FastAPI application & API endpoints
├── Frontend/
│   └── app.py             # Streamlit frontend UI
├── Dataset/
│   └── patients.json      # Patient records (JSON)
├── Dockerfile             # Single-image Docker build
├── start.sh               # Entrypoint script (runs both services)
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** or **Docker**

### Option 1 — Run Locally

1. **Clone the repository**

   ```bash
   git clone https://github.com/archisman2006/patient.git
   cd patient
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI backend**

   ```bash
   cd Backend
   uvicorn main:app --reload
   ```

4. **Start the Streamlit frontend** (in a second terminal)

   ```bash
   cd Frontend
   streamlit run app.py
   ```

5. Open **http://localhost:8501** in your browser.

Or pull the pre-built image:

```bash
docker pull archisman2006/patient
docker run -p 8000:8000 -p 8501:8501 archisman2006/patient
```

Then open **http://localhost:8501** for the UI and **http://localhost:8000/docs** for the interactive API docs.

---

## 📡 API Endpoints

| Method   | Endpoint                | Description               |
| -------- | ----------------------- | ------------------------- |
| `GET`    | `/`                     | Welcome message           |
| `GET`    | `/about`                | About the API             |
| `GET`    | `/view`                 | Get all patients          |
| `GET`    | `/patient/{patient_id}` | Get a single patient      |
| `GET`    | `/sort?sort_by=&order=` | Sort patients             |
| `POST`   | `/create`               | Add a new patient         |
| `PUT`    | `/edit/{patient_id}`    | Update a patient          |
| `DELETE` | `/delete/{patient_id}`  | Delete a patient          |

---

## 📝 License

This is a personal / learning project. Feel free to use it as a reference or starting point for your own work.

---