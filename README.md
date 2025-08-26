🏥 Healthcare Data Pipeline API

An end-to-end healthcare data pipeline that ingests real CQC provider data, cleans and transforms it, generates KPIs and reports, trains a machine learning model, and exposes predictions via a FastAPI microservice.

🚀 Live Demo: Healthcare Pipeline on Render

⚡ Tech Stack: Python · Pandas · Scikit-learn · FastAPI · Docker · Render

📊 Features

✅ Fetches real Care Quality Commission (CQC) healthcare provider directory (UK).

✅ Cleans and standardises provider data into curated and restricted datasets.

✅ Generates KPI summaries and visual reports (PNG charts, TXT summaries).

✅ Trains a simple Logistic Regression model to predict risk of low-quality data.

✅ Exposes predictions via a FastAPI REST API.

✅ Fully containerised with Docker → deployable anywhere.

✅ Live deployment on Render (free tier).

🏗 Architecture
flowchart LR
    A[01_fetch_cqc.py] --> B[02_transform_cqc.py]
    B --> C[03_report.py]
    C --> D[04_ml_train.py]
    D --> E[05_score_api.py]
    E -->|Docker + Render| F[(Public API)]

⚡ Quick Start (Local with Docker)

Clone the repo and build:

git clone https://github.com/YOUR_USERNAME/gew_healthcare_pipeline.git
cd gew_healthcare_pipeline

docker compose build --no-cache
docker compose up


API will be available at:

http://127.0.0.1:9000

🌍 Live API (Render)
Health Check

Open in browser:

https://healthcare-pipeline.onrender.com/health


Response:

{
  "ok": true,
  "cols": ["data_completeness_score", "provider_type_HOSPITAL", ...]
}

Risk Scoring

POST request (example with PowerShell):

Invoke-RestMethod -Method Post -Uri https://healthcare-pipeline.onrender.com/score -ContentType 'application/json' `
  -Body '{"provider_type":"GP_PRACTICE","region":"London","data_completeness_score":0.70}'


Response:

{
  "risk_low_quality": 0.1325
}

📂 Project Structure
gew_healthcare_pipeline/
│
├── data/                     # Raw inputs (CQC CSV)
├── output/                   # Curated, restricted, reports, model
│
├── src/
│   ├── 01_fetch_cqc.py       # Download CQC CSV
│   ├── 02_transform_cqc.py   # Transform + anonymise
│   ├── 03_report.py          # Generate KPIs + charts
│   ├── 04_ml_train.py        # Train ML model
│   ├── 05_score_api.py       # FastAPI service
│
├── requirements.txt
├── entrypoint.py             # Pipeline + API launcher
├── Dockerfile
└── docker-compose.yml

🧑‍💻 Author

Kartik Goswami
📍 Newcastle upon Tyne, UK
🔗 GitHub
 | LinkedIn

⭐ Demo Pitch (for Interview)

“I deployed an end-to-end healthcare data pipeline on Render. It ingests live CQC data, cleans and curates it, generates KPIs, trains a risk model, and serves predictions through a public FastAPI API. For example, when I POST a GP practice in London with 70% data completeness, it returns a risk score of 0.1325.”
