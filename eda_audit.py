
import os
import pandas as pd
import numpy as np
from termcolor import colored

DATA_DIR = "data"
SNAPSHOT_DATE = "2025-09-30"


# ---------------------------------------------------------
# Helper: Pretty section headers
# ---------------------------------------------------------
def section(title):
    print("\n" + colored("=" * 80, "cyan"))
    print(colored(f"{title}", "yellow", attrs=["bold"]))
    print(colored("=" * 80, "cyan"))


# ---------------------------------------------------------
# Load all datasets
# ---------------------------------------------------------
def load_data():
    section("Loading Data Files")

    files = {
        "customers": "customers.csv",
        "churn_labels": "churn_labels.csv",
        "web_events": "web_events_snapshot.csv",
        "tickets": "support_tickets.csv",
        "interventions": "intervention_history.csv",
        "rfm": "rfm_modeling_snapshot.csv",
        "orders": "orders.csv",
    }

    data = {}
    for key, filename in files.items():
        path = os.path.join(DATA_DIR, filename)
        print(f"Loading {filename} ...")
        df = pd.read_csv(path)

        # Apply snapshot filter only to orders
        if key == "orders":
            df["order_date"] = pd.to_datetime(df["order_date"])
            df = df[df["order_date"] >= SNAPSHOT_DATE]

        data[key] = df

    return data


# ---------------------------------------------------------
# Missing Values
# ---------------------------------------------------------
def check_missing(df, name):
    section(f"Missing Values — {name}")
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print(colored("✔ No missing values", "green"))
    else:
        print(missing)


# ---------------------------------------------------------
# Duplicate-like Records
# ---------------------------------------------------------
def check_duplicates(df, name, subset=None):
    section(f"Duplicate-like Records — {name}")

    if subset is None:
        subset = df.columns.tolist()

    dup_count = df.duplicated(subset=subset, keep=False).sum()
    print(f"Duplicate rows (subset={subset}): {dup_count}")


# ---------------------------------------------------------
# Outliers (Orders)
# ---------------------------------------------------------
def check_outliers_orders(df):
    section("Outliers — Orders (gross_amount)")

    q1 = df["gross_amount"].quantile(0.25)
    q3 = df["gross_amount"].quantile(0.75)
    iqr = q3 - q1

    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    print(f"IQR Lower Bound: {lower:.2f}")
    print(f"IQR Upper Bound: {upper:.2f}")

    high = (df["gross_amount"] > upper).sum()
    low = (df["gross_amount"] < lower).sum()

    print(f"High Outliers: {high}")
    print(f"Low Outliers: {low}")


# ---------------------------------------------------------
# Invalid Values
# ---------------------------------------------------------
def check_invalid(data):
    section("Invalid / Suspicious Values")

    # Customers
    customers = data["customers"]
    valid_loyalty = {"Silver", "Gold", "Platinum"}
    valid_skin = {"Normal", "Dry", "Oily", "Combination", "Sensitive"}

    invalid_loyalty = customers[~customers["loyalty_tier"].isin(valid_loyalty)]
    invalid_skin = customers[~customers["skin_type"].isin(valid_skin)]

    print(f"Invalid loyalty_tier: {len(invalid_loyalty)}")
    print(f"Invalid skin_type: {len(invalid_skin)}")

    # Orders
    orders = data["orders"]
    invalid_discount = orders[(orders["discount_pct"] < 0) | (orders["discount_pct"] > 0.7)]
    print(f"Invalid discount_pct: {len(invalid_discount)}")

    # Tickets
    tickets = data["tickets"]
    invalid_sentiment = tickets[(tickets["sentiment_score"] < -1) | (tickets["sentiment_score"] > 1)]
    print(f"Invalid sentiment_score: {len(invalid_sentiment)}")

    # Web events
    web = data["web_events"]
    numeric_cols = [
        "sessions_30d", "product_views_30d", "cart_adds_30d",
        "wishlist_adds_30d", "abandoned_carts_30d",
        "email_opens_30d", "campaign_clicks_30d", "last_visit_days_ago"
    ]
    negatives = (web[numeric_cols] < 0).any(axis=1).sum()
    print(f"Negative numeric values: {negatives}")


# ---------------------------------------------------------
# Join Issues
# ---------------------------------------------------------
def check_join_issues(data):
    section("Join Issues — customer_id Coverage")

    customers = data["customers"]

    def coverage(df, name):
        merged = customers[["customer_id"]].merge(
            df[["customer_id"]].drop_duplicates(),
            on="customer_id",
            how="left",
            indicator=True
        )
        present = (merged["_merge"] == "both").sum()
        missing = (merged["_merge"] == "left_only").sum()
        print(f"{name}: present={present}, missing={missing}")

    coverage(data["churn_labels"], "churn_labels")
    coverage(data["web_events"], "web_events_snapshot")
    coverage(data["tickets"], "support_tickets")
    coverage(data["interventions"], "intervention_history")
    coverage(data["rfm"], "rfm_modeling_snapshot")
    coverage(data["orders"], "orders (>= snapshot date)")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    data = load_data()

    for name, df in data.items():
        check_missing(df, name)
        check_duplicates(df, name, subset=["customer_id"] if "customer_id" in df.columns else None)

    check_outliers_orders(data["orders"])
    check_invalid(data)
    check_join_issues(data)


if __name__ == "__main__":
    main()
