import os, requests
from bs4 import BeautifulSoup
from pathlib import Path

PAGE = "https://www.cqc.org.uk/content/how-get-and-re-use-cqc-information-and-data"
OUT  = Path("data/cqc_locations.csv")

def find_latest_csv():
    html = requests.get(PAGE, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = (a.get_text() or "").lower()
        if href.lower().endswith(".csv") and "directory" in text:
            return href if href.startswith("http") else f"https://www.cqc.org.uk{href}"
    raise SystemExit("❌ Could not find a CSV link. Please update script.")

def main():
    url = os.getenv("CQC_CSV_URL") or find_latest_csv()
    print("⬇️ Downloading:", url)
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(r.content)
    print("✅ Saved ->", OUT.resolve())

if __name__ == "__main__":
    main()
