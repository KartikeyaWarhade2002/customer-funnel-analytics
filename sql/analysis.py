import sqlite3
import pandas as pd

# =====================================================
# Database Connection
# =====================================================

DATABASE = "data/customer_funnel.db"

conn = sqlite3.connect(DATABASE)

print("=" * 100)
print("CUSTOMER FUNNEL ANALYSIS")
print("=" * 100)

# =====================================================
# Query 1
# Overall Funnel Performance
# =====================================================

query_1 = """
SELECT
COUNT(session_id) AS total_sessions,
SUM(viewed_product) AS product_views,
SUM(added_to_cart) AS carts,
SUM(checkout_started) AS checkouts,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(session_id),2
) AS conversion_rate
FROM customer_funnel;
"""

funnel_summary = pd.read_sql_query(query_1, conn)

print("\nOVERALL FUNNEL PERFORMANCE")
print("-" * 80)
print(funnel_summary)

# =====================================================
# Query 2
# Funnel Drop-Off
# =====================================================

query_2 = """
SELECT
ROUND(
100.0 * SUM(viewed_product) / COUNT(session_id),2
) AS view_rate,

ROUND(
100.0 * SUM(added_to_cart) / SUM(viewed_product),2
) AS cart_rate,

ROUND(
100.0 * SUM(checkout_started) / SUM(added_to_cart),2
) AS checkout_rate,

ROUND(
100.0 * SUM(purchase_completed) / SUM(checkout_started),2
) AS purchase_rate
FROM customer_funnel;
"""

dropoff = pd.read_sql_query(query_2, conn)

print("\nFUNNEL CONVERSION RATES")
print("-" * 80)
print(dropoff)

# =====================================================
# Query 3
# Device Performance
# =====================================================

query_3 = """
SELECT
device,
COUNT(*) AS sessions,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(*),2
) AS conversion_rate,
ROUND(
SUM(revenue),2
) AS revenue
FROM customer_funnel
GROUP BY device
ORDER BY conversion_rate DESC;
"""

device = pd.read_sql_query(query_3, conn)

print("\nDEVICE PERFORMANCE")
print("-" * 80)
print(device)

# =====================================================
# Query 4
# Channel Performance
# =====================================================

query_4 = """
SELECT
channel,
COUNT(*) AS sessions,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(*),2
) AS conversion_rate,
ROUND(
SUM(revenue),2
) AS revenue
FROM customer_funnel
GROUP BY channel
ORDER BY revenue DESC;
"""

channel = pd.read_sql_query(query_4, conn)

print("\nCHANNEL PERFORMANCE")
print("-" * 80)
print(channel)

# =====================================================
# Query 5
# Region Performance
# =====================================================

query_5 = """
SELECT
region,
COUNT(*) AS sessions,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(*),2
) AS conversion_rate,
ROUND(
SUM(revenue),2
) AS revenue
FROM customer_funnel
GROUP BY region
ORDER BY revenue DESC;
"""

region = pd.read_sql_query(query_5, conn)

print("\nREGION PERFORMANCE")
print("-" * 80)
print(region)

# =====================================================
# Query 6
# New vs Returning Users
# =====================================================

query_6 = """
SELECT
user_type,
COUNT(*) AS sessions,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(*),2
) AS conversion_rate,
ROUND(
SUM(revenue),2
) AS revenue
FROM customer_funnel
GROUP BY user_type
ORDER BY conversion_rate DESC;
"""

users = pd.read_sql_query(query_6, conn)

print("\nNEW VS RETURNING USERS")
print("-" * 80)
print(users)

# =====================================================
# Query 7
# Discount Impact
# =====================================================

query_7 = """
SELECT
    CASE
        WHEN discount_applied = 1 THEN 'Discount Applied'
        ELSE 'No Discount'
    END AS discount_status,

    COUNT(*) AS sessions,

    SUM(purchase_completed) AS purchases,

    ROUND(
        SUM(revenue),
        2
    ) AS total_revenue,

    ROUND(
        AVG(
            CASE
                WHEN purchase_completed = 1
                THEN order_value
            END
        ),
        2
    ) AS average_order_value

FROM customer_funnel

GROUP BY discount_applied

ORDER BY total_revenue DESC;
"""

discount = pd.read_sql_query(query_7, conn)

print("\nDISCOUNT ANALYSIS")
print("-" * 80)
print(discount)

# =====================================================
# Query 8
# Campaign Performance
# =====================================================

query_8 = """
SELECT
campaign_type,
COUNT(*) AS sessions,
SUM(purchase_completed) AS purchases,
ROUND(
100.0 * SUM(purchase_completed) / COUNT(*),2
) AS conversion_rate,
ROUND(
SUM(revenue),2
) AS revenue
FROM customer_funnel
GROUP BY campaign_type
ORDER BY revenue DESC;
"""

campaign = pd.read_sql_query(query_8, conn)

print("\nCAMPAIGN PERFORMANCE")
print("-" * 80)
print(campaign)

print("\nAnalysis Complete.")

conn.close()