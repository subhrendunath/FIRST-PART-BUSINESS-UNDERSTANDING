import os
from pathlib import Path
import gdown

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

FOLDER_URL = "https://drive.google.com/drive/folders/1PmLapJI1VSDgvl_AxARNKwM1MCd3WFX0"

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# DOWNLOAD ENTIRE FOLDER
# --------------------------------------------------

print("Downloading files from Google Drive...")

gdown.download_folder(
    url=FOLDER_URL,
    output=str(DATA_DIR),
    quiet=False,
    use_cookies=False
)

print("Download completed.")

# --------------------------------------------------
# VERIFY FILES
# --------------------------------------------------

required_files = [
    "customers.csv",
    "orders.csv",
    "support_tickets.csv",
    "web_events_snapshot.csv",
    "churn_labels.csv",
    "rfm_modeling_snapshot.csv",
    "intervention_history.csv"
]

print("\nChecking downloaded files:")

for file in required_files:
    path = DATA_DIR / file

    if path.exists():
        print(f"✓ {file}")
    else:
        print(f"✗ Missing: {file}")
