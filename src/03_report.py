import pandas as pd, matplotlib.pyplot as plt
from pathlib import Path

CUR = Path("output/curated/provider_core.csv")
OUT = Path("output/reports"); OUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(CUR)

total = len(df)
mean_comp = round(df["data_completeness_score"].mean(), 3)
by_type = df.groupby("provider_type")["provider_id"].count().sort_values(ascending=False)

(OUT / "kpi_summary.txt").write_text(
    f"Total providers: {total}\n"
    f"Mean data completeness: {mean_comp}\n"
    f"Providers by type:\n{by_type.to_string()}\n",
    encoding="utf-8"
)

df.groupby("region")["data_completeness_score"].mean().sort_values().plot(kind="bar").figure.savefig(OUT / "completeness_by_region.png")
df["provider_type"].value_counts().plot(kind="bar").figure.savefig(OUT / "provider_type_counts.png")

print("✅ Reports written to:", OUT)
