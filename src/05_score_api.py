from fastapi import FastAPI, HTTPException
import pandas as pd, joblib, os

PKL = "output/model_quality.pkl"
app = FastAPI(title="Healthcare Quality Scoring API")

if os.path.exists(PKL):
    pack = joblib.load(PKL)
    model, cols = pack["model"], pack["cols"]
else:
    model, cols = None, []
    print("⚠️ No model found. Run 04_ml_train.py first.")

@app.get("/health")
def health():
    return {"ok": model is not None, "cols": cols}

@app.post("/score")
def score(payload: dict):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not trained")
    X = pd.DataFrame([payload])
    X = pd.get_dummies(X)
    for c in cols:
        if c not in X.columns: X[c] = 0
    X = X[cols]
    prob = float(model.predict_proba(X)[:,1][0])
    return {"risk_low_quality": round(prob,4)}
