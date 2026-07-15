from pathlib import Path

import pandas as pd

# =====================================================
# Paths
# =====================================================

INPUT_FILE = Path("data/processed/customer_funnel_clean.csv")
OUTPUT_FILE = Path("data/processed/customer_funnel_powerbi.csv")

# =====================================================
# Read Data
# =====================================================

df = pd.read_csv(
    INPUT_FILE,
    parse_dates=["date"]
)

# =====================================================
# Create Additional Columns
# =====================================================

df["Year"] = df["date"].dt.year
df["Month Name"] = df["date"].dt.strftime("%B")
df["Month Number"] = df["date"].dt.month
df["Day"] = df["date"].dt.day

# =====================================================
# Save
# =====================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("=" * 60)
print("POWER BI DATASET CREATED")
print("=" * 60)
print(df.shape)
print(OUTPUT_FILE)