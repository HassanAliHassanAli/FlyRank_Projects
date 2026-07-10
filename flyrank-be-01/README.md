# FlyRank Backend AI Internship: Assignment BE-01

## 📌 Overview
This repository contains the first assignment (BE-01) for the **FlyRank AI Internship Program**. The goal of this project is to build a foundational backend server with two distinct JSON endpoints using Python and FastAPI.

## 👨‍💻 Author
**Hassan Ali**  
*Backend AI Engineering Intern @ FlyRank AI*

## 🛠️ Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **ASGI Server:** Uvicorn

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/flyrank-be-01.git
   cd flyrank-be-01
   ```

2. **Install the required dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Start the server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

4. **Access the API:**
   Open your browser or use `curl` to visit:
   - `http://127.0.0.1:8000`
   - `http://127.0.0.1:8000/status`

## 📡 API Endpoints

| Method | Endpoint  | Description |
|--------|-----------|-------------|
| `GET`  | `/`       | Returns a welcome message. |
| `GET`  | `/status` | Returns the server active status and intern level (Builder). |

## 💡 Notes
This project is part of the Week 1 Setup phase to establish server-side request/response loops and version control workflows.