from pathlib import Path
import sqlite3
import pandas as pd

# =====================================================
# Paths
# =====================================================

RAW_FILE = Path("data/raw/d2c_marketing_funnel_data.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_FILE = PROCESSED_DIR / "customer_funnel_clean.csv"
DATABASE_FILE = Path("data/customer_funnel.db")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Read Dataset
# =====================================================

df = pd.read_csv(RAW_FILE)

print("=" * 100)
print("CUSTOMER FUNNEL ETL")
print("=" * 100)

# =====================================================
# Convert Date
# =====================================================

df["date"] = pd.to_datetime(df["date"])

# =====================================================
# Standardize Text Columns
# =====================================================

text_columns = [
    "channel",
    "campaign_type",
    "device",
    "user_type",
    "region",
    "visited_website",
    "viewed_product",
    "added_to_cart",
    "checkout_started",
    "purchase_completed",
    "discount_applied"
]

for col in text_columns:
    df[col] = df[col].astype(str).str.strip()

# =====================================================
# Convert Funnel Columns to 1 / 0
# =====================================================

funnel_columns = [
    "visited_website",
    "viewed_product",
    "added_to_cart",
    "checkout_started",
    "purchase_completed",
    "discount_applied"
]

for col in funnel_columns:
    df[col] = df[col].map({
        "Yes": 1,
        "No": 0
    })

# =====================================================
# Funnel Validation
# =====================================================

invalid_view = (
    (df["added_to_cart"] == 1) &
    (df["viewed_product"] == 0)
).sum()

invalid_checkout = (
    (df["checkout_started"] == 1) &
    (df["added_to_cart"] == 0)
).sum()

invalid_purchase = (
    (df["purchase_completed"] == 1) &
    (df["checkout_started"] == 0)
).sum()

print("\nFunnel Validation")
print("-" * 40)

print(f"Cart without Product View : {invalid_view}")
print(f"Checkout without Cart     : {invalid_checkout}")
print(f"Purchase without Checkout : {invalid_purchase}")

# =====================================================
# Additional Columns
# =====================================================

df["conversion"] = df["purchase_completed"]

df["cart_abandonment"] = (
    (df["added_to_cart"] == 1) &
    (df["purchase_completed"] == 0)
).astype(int)

# =====================================================
# Save Clean CSV
# =====================================================

df.to_csv(
    PROCESSED_FILE,
    index=False
)

# =====================================================
# SQLite Database
# =====================================================

conn = sqlite3.connect(DATABASE_FILE)

df.to_sql(
    "customer_funnel",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

# =====================================================
# Summary
# =====================================================

print("\nDataset Summary")
print("-" * 40)

print(f"Rows                 : {len(df):,}")
print(f"Columns              : {len(df.columns)}")
print(f"Unique Users         : {df['user_id'].nunique():,}")
print(f"Unique Sessions      : {df['session_id'].nunique():,}")

print("\nFiles Created")
print("-" * 40)

print(PROCESSED_FILE)
print(DATABASE_FILE)

print("\nETL Completed Successfully.")