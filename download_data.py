"""Download public IBM Skills Network datasets used in the SpaceX capstone."""
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

BASE = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/"
FILES = [
    "dataset_part_1.csv",
    "dataset_part_2.csv",
    "dataset_part_3.csv",
    "spacex_launch_dash.csv",
    "spacex_launch_geo.csv",
    "spacex_web_scraped.csv",
]

def main():
    for filename in FILES:
        url = BASE + filename
        target = DATA / filename
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            if not response.content:
                raise ValueError("Downloaded file is empty.")
            target.write_bytes(response.content)
            print(f"Downloaded {filename} ({len(response.content):,} bytes)")
        except Exception as exc:
            print(f"Could not download {filename}: {exc}")
            print(f"If you have this CSV from Coursera, save it to: {target}")
    print(f"\nData folder: {DATA}")

if __name__ == "__main__":
    main()
