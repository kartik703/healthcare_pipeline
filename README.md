#  Healthcare Data Pipeline API

[![Live API](https://img.shields.io/badge/Live_API-Render-blue)](https://healthcare-pipeline.onrender.com/health)

A complete, end-to-end healthcare data engineering pipeline that:

- ingests real CQC (Care Quality Commission) data,
- performs cleaning and transformation,
- generates analytics and reports,
- trains a machine learning model to assess data quality risk,
- and serves real-time predictions through a **FastAPI** interface, all packaged in Docker and deployed on **Render**.

---

##  Live Demo

| Endpoint | Description |
|----------|-------------|
| [`/health`](https://healthcare-pipeline.onrender.com/health) | Check if the ML model is loaded and view expected input features. |
| `/score` | POST JSON payload to receive a `risk_low_quality` score. |

Example scoring request:


Invoke-RestMethod -Method Post -Uri https://healthcare-pipeline.onrender.com/score -ContentType 'application/json' `
  -Body '{"provider_type":"GP_PRACTICE","region":"London","data_completeness_score":0.70}'
Expected JSON response:


Edit
{
  "risk_low_quality": 0.1325
}
Project Overview
This pipeline comprises the following key components implemented in Python and containerized for portability:


Edit
src/
├── 01_fetch_cqc.py        # Downloads latest CQC provider directory
├── 02_transform_cqc.py    # Cleans and standardizes data, anonymizes sensitive fields
├── 03_report.py           # Creates KPI summaries and charts
├── 04_ml_train.py         # Trains an ML model to flag low-quality data (with synthetic fallback)
└── 05_score_api.py        # Exposes the model via FastAPI for live scoring
Supporting infrastructure files include:

entrypoint.py: One-click orchestration of all pipeline steps + API launch.

Dockerfile + docker-compose.yml: For local and cloud deployments.

requirements.txt: Specifies all necessary dependencies.

Local Setup with Docker
To run the entire pipeline locally from start to finish, follow these steps:


git clone https://github.com/kartik703/healthcare_pipeline.git
cd healthcare_pipeline
docker compose build --no-cache
docker compose up
Once running, you’ll have a locally hosted API available at http://127.0.0.1:9000.

Deployed on Render
The pipeline is live and accessible via HTTPS:

Health Endpoint: https://healthcare-pipeline.onrender.com/health

Prediction Endpoint: POST https://healthcare-pipeline.onrender.com/score

Architecture Overview
flowchart LR
    A[01_fetch_cqc.py] --> B[02_transform_cqc.py]
    B --> C[03_report.py]
    C --> D[04_ml_train.py]
    D --> E[05_score_api.py]
    E ==> F(Dockerized Service)
    F --> G(Render Deployment)
Tech Stack
Languages & Libraries: Python, Pandas, Scikit-Learn, FastAPI, Joblib

Visualization: Matplotlib

Containerization: Docker

Hosting: Render Deployment

Development Tools: Git, GitHub

How to Use This Project
Cloning and Local Development
bash
Copy
Edit
git clone https://github.com/kartik703/healthcare_pipeline.git
cd healthcare_pipeline
Run Locally via Docker
bash
Copy
Edit
docker compose build
docker compose up
Test Locally
bash
Copy
Edit
curl -X GET http://127.0.0.1:9000/health

curl -X POST http://127.0.0.1:9000/score \
     -H "Content-Type: application/json" \
     -d '{"provider_type":"GP_PRACTICE","region":"London","data_completeness_score":0.70}'
View in Browser
Visit https://healthcare-pipeline.onrender.com/health
