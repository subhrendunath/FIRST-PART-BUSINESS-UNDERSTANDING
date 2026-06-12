import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

DATA_DIR = Path("data")

# --------------------------------------------------
# VIEW FILES
# --------------------------------------------------

files_to_view = [
    "customers.csv",
    "orders.csv",
    "support_tickets.csv",
    "web_events_snapshot.csv",
    "churn_labels.csv",
    "rfm_modeling_snapshot.csv",
    "intervention_history.csv"
]

for file in files_to_view:
    file_path = DATA_DIR / file
    
    if file_path.exists():
        print(f"\n{'='*60}")
        print(f"FILE: {file}")
        print(f"{'='*60}")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Display basic info
        print(f"Shape: {df.shape} (rows, columns)")
        print(f"\nFirst few rows:")
        print(df.head())
        
        print(f"\nData types:")
        print(df.dtypes)
        
        print(f"\nBasic statistics:")
        print(df.describe())
        
        print(f"\nMissing values:")
        print(df.isnull().sum())
    else:
        print(f"✗ File not found: {file}")
