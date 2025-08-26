import pandas as pd, joblib, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

df = pd.read_csv("output/curated/provider_core.csv")

df["low_quality"] = (df["data_completeness_score"] <= 0.75).astype(int)

if df["low_quality"].nunique() < 2:
    print("⚠️ Only one class. Injecting 10% synthetic low-quality for demo...")
    np.random.seed(42)
    df["low_quality"] = np.where(np.random.rand(len(df)) < 0.1, 1, 0)

X = pd.get_dummies(df[["provider_type","region","data_completeness_score"]], drop_first=True)
y = df["low_quality"]

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
clf = LogisticRegression(max_iter=1000)
clf.fit(Xtr, ytr)
auc = roc_auc_score(yte, clf.predict_proba(Xte)[:,1])
print("AUC:", round(auc,3))

joblib.dump({"model": clf, "cols": X.columns.tolist()}, "output/model_quality.pkl")
print("✅ Model saved -> output/model_quality.pkl")
