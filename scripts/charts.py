from pathlib import Path

import pandas as pd
import plotly.express as px

# =====================================================
# Paths
# =====================================================

INPUT_FILE = Path("data/processed/customer_funnel_clean.csv")
OUTPUT_DIR = Path("charts")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =====================================================
# Read Dataset
# =====================================================

df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

# =====================================================
# Common Layout
# =====================================================

LAYOUT = dict(
    template="plotly_white",
    font=dict(size=16),
    title_x=0.5
)

# =====================================================
# Chart 1
# Funnel Overview
# =====================================================

funnel = pd.DataFrame({
    "Stage": [
        "Website Visit",
        "Product View",
        "Add to Cart",
        "Checkout",
        "Purchase"
    ],
    "Users": [
        len(df),
        df["viewed_product"].sum(),
        df["added_to_cart"].sum(),
        df["checkout_started"].sum(),
        df["purchase_completed"].sum()
    ]
})

fig = px.funnel(
    funnel,
    x="Users",
    y="Stage",
    title="Customer Purchase Funnel"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "01_customer_funnel.png",
    width=1400,
    height=800
)

# =====================================================
# Chart 2
# Conversion by Device
# =====================================================

device = (
    df.groupby("device")
    .agg(
        Sessions=("session_id", "count"),
        Purchases=("purchase_completed", "sum")
    )
    .reset_index()
)

device["Conversion Rate"] = (
    device["Purchases"] /
    device["Sessions"] * 100
).round(2)

fig = px.bar(
    device,
    x="device",
    y="Conversion Rate",
    color="device",
    text="Conversion Rate",
    title="Conversion Rate by Device"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "02_device_conversion.png",
    width=1400,
    height=800
)

# =====================================================
# Chart 3
# Conversion by Marketing Channel
# =====================================================

channel = (
    df.groupby("channel")
    .agg(
        Sessions=("session_id", "count"),
        Purchases=("purchase_completed", "sum")
    )
    .reset_index()
)

channel["Conversion Rate"] = (
    channel["Purchases"] /
    channel["Sessions"] * 100
).round(2)

fig = px.bar(
    channel,
    x="channel",
    y="Conversion Rate",
    color="channel",
    text="Conversion Rate",
    title="Conversion Rate by Marketing Channel"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "03_channel_conversion.png",
    width=1400,
    height=800
)

# =====================================================
# Chart 4
# Revenue by Campaign
# =====================================================

campaign = (
    df.groupby("campaign_type")["revenue"]
    .sum()
    .reset_index()
    .sort_values(
        by="revenue",
        ascending=False
    )
)

fig = px.bar(
    campaign,
    x="campaign_type",
    y="revenue",
    color="campaign_type",
    text_auto=".2s",
    title="Revenue by Campaign Type"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "04_campaign_revenue.png",
    width=1400,
    height=800
)

# =====================================================
# Chart 5
# Revenue by Region
# =====================================================

region = (
    df.groupby("region")["revenue"]
    .sum()
    .reset_index()
)

fig = px.pie(
    region,
    names="region",
    values="revenue",
    title="Revenue Contribution by Region"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "05_region_revenue.png",
    width=1400,
    height=800
)

# =====================================================
# Chart 6
# New vs Returning Users
# =====================================================

users = (
    df.groupby("user_type")
    .agg(
        Sessions=("session_id", "count"),
        Purchases=("purchase_completed", "sum")
    )
    .reset_index()
)

users["Conversion Rate"] = (
    users["Purchases"] /
    users["Sessions"] * 100
).round(2)

fig = px.bar(
    users,
    x="user_type",
    y="Conversion Rate",
    color="user_type",
    text="Conversion Rate",
    title="Conversion Rate by User Type"
)

fig.update_layout(**LAYOUT)

fig.write_image(
    OUTPUT_DIR / "06_user_conversion.png",
    width=1400,
    height=800
)

print("=" * 70)
print("PLOTLY CHARTS CREATED SUCCESSFULLY")
print("=" * 70)

for file in sorted(OUTPUT_DIR.glob("*.png")):
    print(file.name)