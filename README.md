# Resume Tuner

An intelligent resume analyzer built with **FastAPI**, **Crew AI**, and **LLM** for parsing resumes via Server-Sent Events (SSE), saving extracted data, and tuning resumes with job descriptions (TODO).

---

## Features

- FastAPI backend with SSE for real-time parsing updates  
- LLM-based parsing of existing resumes into structured data using **Crew AI** multi-agent orchestration  
- Save extracted resume data to database  
- Job description based resume tuning (planned)  

---

## Setup & Run

> **Note:** You need to create a `.env` file containing API keys and secrets as shown in the `.env-example` file.

```bash
git clone https://github.com/your-username/resume-tuner.git
cd resume-tuner
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload
