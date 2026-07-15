from pathlib import Path

import pandas as pd

# =====================================================
# Paths
# =====================================================

INPUT_FILE = Path("data/processed/customer_funnel_clean.csv")
OUTPUT_FILE = Path("excel/customer_funnel_analysis.xlsx")

# =====================================================
# Read Dataset
# =====================================================

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["date"]
)

# =====================================================
# Create Date Columns
# =====================================================

df["Year"] = df["date"].dt.year
df["Month"] = df["date"].dt.strftime("%B")
df["Month Number"] = df["date"].dt.month
df["Day"] = df["date"].dt.day

# =====================================================
# Rename Columns
# =====================================================

df = df.rename(columns={
    "user_id": "User ID",
    "session_id": "Session ID",
    "date": "Date",
    "channel": "Channel",
    "campaign_type": "Campaign Type",
    "device": "Device",
    "user_type": "User Type",
    "region": "Region",
    "viewed_product": "Viewed Product",
    "added_to_cart": "Added To Cart",
    "checkout_started": "Checkout Started",
    "purchase_completed": "Purchase Completed",
    "discount_applied": "Discount Applied",
    "order_value": "Order Value",
    "revenue": "Revenue"
})

# =====================================================
# Save Excel
# =====================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Data",
        index=False
    )

print("=" * 60)
print("Excel dataset created successfully.")
print(f"Rows    : {len(df):,}")
print(f"Columns : {len(df.columns)}")
print(f"Saved to: {OUTPUT_FILE}")
print("=" * 60)