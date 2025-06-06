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


### Register User  
API Endpoints

All endpoints accept POST requests. JSON payload is expected unless otherwise noted (e.g., file upload).
1. Register User

POST /v1/auth/register

Creates a new user account with email, name, and password. This allows the user to access authenticated services like uploading resumes or tuning them.

Request Body Example:

{
  "email": "user@example.com",
  "name": "abc",
  "password": "yourpassword"
}

Response: Confirmation message or error if the user already exists.
2. User Login

POST /v1/auth/login

Authenticates a user by email and password. Returns an access token for authenticated endpoints.

Request Body Example:

{
  "email": "user@example.com",
  "password": "yourpassword"
}

Response: Access token (e.g., JWT) for authenticated requests.
3. Upload Resume

POST /v1/resume/upload

Allows uploading of a resume file (PDF, DOCX, etc.). The backend parses the resume using LLM agents and streams real-time parsing updates using Server-Sent Events (SSE).

Form Data:

    file: The resume file to upload.

Response: Parsing progress streamed over SSE, and final parsed structured data saved to the database.
4. Add Job Description

POST /v1/job-description/add

Add a new job description associated with a company. This can be later used for tuning resumes to match the job requirements.

Request Body Example:

{
  "company_name": "test",
  "job_description": "Job description text here."
}

Response: Confirmation of job description saved.
5. Tune Resume (Planned)

POST /v1/resume/tune

Requests AI-based tuning of an existing resume to better align it with a specific job description. This feature is planned and may not yet be implemented.

Request Body Example:

{
  "resume_id": 1,
  "job_description_id": 2,
  "comment": "Tune my resume don't lie"
}

Response: Confirmation that tuning has started or is queued.
6. Generate Resume

POST /v1/resume/generate

Generates a new or updated resume document based on the parsed and/or tuned data stored in the system.

Request Body Example:

{
  "resume_id": 3
}

Response: Download link or data of the generated resume.
Notes

    Include authentication tokens in request headers for protected endpoints after login is implemented.

    SSE is used for real-time streaming of parsing progress during resume uploads.

    Resume upload endpoint requires multipart/form-data encoding for the file upload.
