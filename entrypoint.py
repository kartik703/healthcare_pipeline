import os, subprocess

steps = [
    "python src/01_fetch_cqc.py",
    "python src/02_transform_cqc.py",
    "python src/03_report.py",
    "python src/04_ml_train.py",
    "uvicorn src.05_score_api:app --host 0.0.0.0 --port 9000"
]

for cmd in steps[:-1]:
    print(f"\n=== Running: {cmd} ===")
    subprocess.run(cmd, shell=True, check=True)

print("\n=== Starting API Server ===")
os.execvp("uvicorn", ["uvicorn", "src.05_score_api:app", "--host", "0.0.0.0", "--port", "9000"])
