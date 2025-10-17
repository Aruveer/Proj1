# 🌟 PROJECT 1: LLM Code Deployment Service (Student API)

This repository contains the source code for the student-built API designed to receive evaluation tasks, generate minimal applications using an LLM, deploy them to GitHub Pages, and notify the evaluation server.

---

## 📝 Project Overview

This API serves as the backend for the "LLM Code Deployment" project. It automates the full DevOps pipeline:

* **Task Reception:** Accepts a `POST` request with task parameters (brief, secret, checks).
* **Validation:** Verifies the `STUDENT_SECRET`.
* **Code Generation:** Uses the **Gemini API** to generate the required application files (HTML, JS, CSS, README, LICENSE).
* **Deployment:** Interacts with the **GitHub API** to create a public repository, push the generated code, and activate **GitHub Pages**.
* **Notification:** Notifies the official evaluation server upon successful deployment.
* **Revision (Round 2):** Handles subsequent requests to update and redeploy the existing application.

---

## ⚙️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | **FastAPI** | Creates the high-performance, asynchronous API endpoint (`/handle_task`). |
| **LLM Integration** | **Google GenAI SDK** (Gemini 2.5 Flash) | Generates application code and content based on the task brief. |
| **Deployment** | **PyGithub** | Handles all interactions with the GitHub API (repo creation, file commits, Pages setup). |
| **Environment** | **Docker** (Hugging Face) | Ensures a consistent, persistent runtime environment for the server. |
| **Persistence** | In-memory Python Dictionary | Stores task metadata (repo URL, nonce) between Round 1 and Round 2 requests. |

---

## 🚀 Setup and Deployment Instructions

This service is designed to be deployed using Hugging Face Spaces via Docker.

### 1. Local Setup (For Development/Testing)

To run locally, ensure Python 3.11+ and all dependencies are installed:

## Set Environment Variables (CRITICAL)

Replace placeholders with your actual secrets. Use a Classic PAT for GitHub.
$env:STUDENT_SECRET = "project"
$env:GITHUB_TOKEN = "your_personal_access_token"
$env:GEMINI_API_KEY = "your_gemini_api_key"

Run the server

Bash

python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
2. Hugging Face Deployment (Production)
The service is hosted on Hugging Face using the provided Dockerfile. The setup relies entirely on Secrets for credentials.

Files Uploaded: main.py, github_utils.py, requirements.txt, Dockerfile.

Secrets Set: STUDENT_SECRET, GITHUB_TOKEN, and GEMINI_API_KEY are stored securely in the Space settings.

Endpoint: The live API is accessible at the public URL: https://[owner]-[space-name].hf.space/handle_task

3. API Details
The single public endpoint accepts a JSON payload via POST:

Endpoint: /handle_task

Method: POST

Request Body: Must conform to the TaskRequest Pydantic model (includes secret, task, round, brief, etc.).

Success Response: HTTP 200 with status JSON.

Failure Response: HTTP 401 (Invalid Secret), HTTP 400 (Bad Payload), or HTTP 500 (Deployment/API Error).
```bash
# Install dependencies
pip install fastapi uvicorn pydantic requests PyGithub google-genai
