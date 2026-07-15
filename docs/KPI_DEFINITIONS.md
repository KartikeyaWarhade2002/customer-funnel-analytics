# KPI Definitions

## Table Grain

**1 Row = 1 Customer Session**

---

## Total Sessions

**Definition**

COUNT(session_id)

---

## Product Views

**Definition**

SUM(viewed_product)

---

## Add to Cart

**Definition**

SUM(added_to_cart)

---

## Checkout Started

**Definition**

SUM(checkout_started)

---

## Purchases

**Definition**

SUM(purchase_completed)

---

## Funnel Conversion Rate

**Definition**

Purchases
/
Total Sessions

---

## Product View Rate

**Definition**

Product Views
/
Total Sessions

---

## Add-to-Cart Rate

**Definition**

Add to Cart
/
Product Views

---

## Checkout Rate

**Definition**

Checkout Started
/
Add to Cart

---

## Purchase Rate

**Definition**

Purchases
/
Checkout Started

---

## Revenue

**Definition**

SUM(revenue)

---

## Average Order Value (AOV)

**Definition**

AVG(order_value)
WHERE purchase_completed = 1

---

## Device Conversion Rate

**Definition**

Purchases
/
Sessions
GROUP BY device

---

## Marketing Channel Conversion Rate

**Definition**

Purchases
/
Sessions
GROUP BY channel

---

## Campaign Conversion Rate

**Definition**

Purchases
/
Sessions
GROUP BY campaign_type

---

## Regional Conversion Rate

**Definition**

Purchases
/
Sessions
GROUP BY region

---

## New User Conversion Rate

**Definition**

Purchases
/
Sessions
WHERE user_type = 'New'

---

## Returning User Conversion Rate

**Definition**

Purchases
/
Sessions
WHERE user_type = 'Returning'
