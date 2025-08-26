import hashlib, pandas as pd
from pathlib import Path

RAW = Path("data/cqc_locations.csv")
CUR = Path("output/curated/provider_core.csv")
RES = Path("output/restricted/provider_contact.csv")
QUA = Path("output/quarantine/bad_rows.csv")

def sha256(x):
    if pd.isna(x) or str(x).strip()=="":
        return None
    return hashlib.sha256(str(x).encode("utf-8")).hexdigest()

def map_type(cat: str) -> str:
    s = (cat or "").lower()
    if "gp" in s: return "GP_PRACTICE"
    if "mental" in s: return "MENTAL_HEALTH_CLINIC"
    if "hospital" in s or "nursing" in s: return "HOSPITAL"
    if "homecare" in s: return "HOMECARE"
    return "OTHER"

def main():
    df = pd.read_csv(RAW, dtype=str, encoding="utf-8-sig", header=4)

    df_core = pd.DataFrame({
        "provider_id": df["CQC Location ID (for office use only)"].astype(str).str.strip(),
        "name": df["Name"].astype(str).str.strip(),
        "provider_type": df["Service types"].astype(str).map(map_type),
        "region": df["Region"].astype(str).str.strip(),
        "registration_status": "Registered",
        "address1": df["Address"].astype(str).str.strip(),
        "town": df["Local authority"].astype(str).str.strip(),
        "postcode": df["Postcode"].astype(str).str.upper().str.replace(" ", "", regex=False),
        "phone": df["Phone number"].astype(str).str.strip(),
        "website": df["Service's website (if available)"].astype(str).str.strip(),
    })

    req = ["address1","postcode","phone"]
    df_core["data_completeness_score"] = df_core[req].replace({"": None}).notna().sum(axis=1) / len(req)

    df_core["address_full"] = df_core[["address1","postcode"]].fillna("").agg(", ".join, axis=1).str.strip(", ")
    df_pii = df_core[["provider_id","phone","address_full"]].copy()
    df_pii["phone_hash"] = df_pii["phone"].apply(sha256)
    df_pii["address_hash"] = df_pii["address_full"].apply(sha256)
    df_pii = df_pii[["provider_id","phone_hash","address_hash"]]

    core = df_core[["provider_id","name","provider_type","region","data_completeness_score","registration_status"]].copy()

    allowed = {"GP_PRACTICE","MENTAL_HEALTH_CLINIC","HOSPITAL","HOMECARE","OTHER"}
    bad = core[(core["provider_id"].isna()) | (~core["provider_type"].isin(allowed))]
    if len(bad):
        QUA.parent.mkdir(parents=True, exist_ok=True)
        bad.to_csv(QUA, index=False)

    core = core.drop(bad.index)

    CUR.parent.mkdir(parents=True, exist_ok=True)
    RES.parent.mkdir(parents=True, exist_ok=True)
    core.to_csv(CUR, index=False)
    df_pii.to_csv(RES, index=False)
    print("✅ Wrote curated & restricted datasets.")

if __name__ == "__main__":
    main()
