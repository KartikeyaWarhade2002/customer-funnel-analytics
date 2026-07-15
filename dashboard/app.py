from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Customer Funnel Analysis",
    page_icon="🛒",
    layout="wide"
)

# =====================================================
# Load Data
# =====================================================

DATA_FILE = Path("data/processed/customer_funnel_clean.csv")

df = pd.read_csv(
    DATA_FILE,
    parse_dates=["date"]
)

# =====================================================
# KPIs
# =====================================================

total_sessions = len(df)
product_views = df["viewed_product"].sum()
add_to_cart = df["added_to_cart"].sum()
checkouts = df["checkout_started"].sum()
purchases = df["purchase_completed"].sum()

conversion_rate = purchases / total_sessions * 100
total_revenue = df["revenue"].sum()

average_order_value = (
    df.loc[df["purchase_completed"] == 1, "order_value"]
    .mean()
)

# =====================================================
# Sidebar
# =====================================================

st.sidebar.title("Filters")

channel = st.sidebar.multiselect(
    "Channel",
    sorted(df["channel"].unique()),
    default=sorted(df["channel"].unique())
)

device = st.sidebar.multiselect(
    "Device",
    sorted(df["device"].unique()),
    default=sorted(df["device"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

user_type = st.sidebar.multiselect(
    "User Type",
    sorted(df["user_type"].unique()),
    default=sorted(df["user_type"].unique())
)

df = df[
    (df["channel"].isin(channel)) &
    (df["device"].isin(device)) &
    (df["region"].isin(region)) &
    (df["user_type"].isin(user_type))
]

# =====================================================
# Title
# =====================================================

st.title("Customer Funnel Analysis Dashboard")

# =====================================================
# KPI Cards
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Revenue",
    f"${total_revenue:,.0f}"
)

c2.metric(
    "Sessions",
    f"{total_sessions:,}"
)

c3.metric(
    "Purchases",
    f"{purchases:,}"
)

c4.metric(
    "Conversion",
    f"{conversion_rate:.2f}%"
)

st.divider()

# =====================================================
# Tabs
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Marketing",
    "Customer",
    "Funnel"
])

# =====================================================
# Executive
# =====================================================

with tab1:

    funnel = pd.DataFrame({
        "Stage": [
            "Website Visit",
            "Product View",
            "Add To Cart",
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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Marketing
# =====================================================

with tab2:

    revenue = (
        df.groupby("channel")["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue,
        x="channel",
        y="revenue",
        color="channel",
        title="Revenue by Channel"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    campaign = (
        df.groupby("campaign_type")["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        campaign,
        x="campaign_type",
        y="revenue",
        color="campaign_type",
        title="Revenue by Campaign"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Customer
# =====================================================

with tab3:

    device_df = (
        df.groupby("device")
        .agg(
            Sessions=("session_id","count"),
            Purchases=("purchase_completed","sum")
        )
        .reset_index()
    )

    device_df["Conversion Rate"] = (
        device_df["Purchases"] /
        device_df["Sessions"] * 100
    )

    fig = px.bar(
        device_df,
        x="device",
        y="Conversion Rate",
        color="device",
        title="Conversion by Device"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    user_df = (
        df.groupby("user_type")
        .agg(
            Sessions=("session_id","count"),
            Purchases=("purchase_completed","sum")
        )
        .reset_index()
    )

    user_df["Conversion Rate"] = (
        user_df["Purchases"] /
        user_df["Sessions"] * 100
    )

    fig = px.bar(
        user_df,
        x="user_type",
        y="Conversion Rate",
        color="user_type",
        title="Conversion by User Type"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# Funnel
# =====================================================

with tab4:

    discount = (
        df.groupby("discount_applied")["revenue"]
        .sum()
        .reset_index()
    )

    discount["discount_applied"] = discount[
        "discount_applied"
    ].map({
        0: "No Discount",
        1: "Discount Applied"
    })

    fig = px.bar(
        discount,
        x="discount_applied",
        y="revenue",
        color="discount_applied",
        title="Revenue by Discount"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    region_df = (
        df.groupby("region")["revenue"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_df,
        names="region",
        values="revenue",
        title="Revenue by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )