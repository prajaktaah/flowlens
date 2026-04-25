"""
User Journey Funnel Analysis — Core Analysis
=============================================
Now upgraded with SQL (SQLite) for data extraction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings, os
import sqlite3

warnings.filterwarnings("ignore")
os.makedirs("outputs", exist_ok=True)

FUNNEL_STEPS = ["visit", "signup", "add_to_cart", "checkout", "purchase"]
STEP_LABELS  = ["Visit", "Sign Up", "Add to Cart", "Checkout", "Purchase"]

PALETTE = {
    "primary":   "#0F4C81",
    "accent":    "#FF6B35",
    "success":   "#2ECC71",
    "danger":    "#E74C3C",
    "warning":   "#F39C12",
    "neutral":   "#95A5A6",
    "bg":        "#F8F9FA",
}

# ─── Load Data into SQLite ────────────────────────────────────────────────

conn = sqlite3.connect("funnel.db")

df = pd.read_csv("data/user_events.csv", parse_dates=["timestamp"])
df.to_sql("events", conn, if_exists="replace", index=False)

# ─── SQL: Funnel Data ─────────────────────────────────────────────────────

funnel_query = """
SELECT 
    step,
    COUNT(DISTINCT user_id) AS users,
    MIN(step_order) as step_order
FROM events
GROUP BY step
ORDER BY step_order
"""
funnel = pd.read_sql(funnel_query, conn)

# ─── SQL: Segment Data ────────────────────────────────────────────────────

dev_df = pd.read_sql("""
SELECT device, step, COUNT(DISTINCT user_id) as users
FROM events
GROUP BY device, step
""", conn)

chan_df = pd.read_sql("""
SELECT channel, step, COUNT(DISTINCT user_id) as users
FROM events
GROUP BY channel, step
""", conn)

age_df = pd.read_sql("""
SELECT age_group, step, COUNT(DISTINCT user_id) as users
FROM events
GROUP BY age_group, step
""", conn)

ctr_df = pd.read_sql("""
SELECT country, step, COUNT(DISTINCT user_id) as users
FROM events
GROUP BY country, step
""", conn)

# ─── 1. Overall Funnel Metrics ─────────────────────────────────────────────

print("=" * 55)
print("  USER JOURNEY FUNNEL ANALYSIS  — SUMMARY REPORT")
print("=" * 55)

total_visitors = funnel.loc[funnel["step"] == "visit", "users"].values[0]
total_buyers   = funnel.loc[funnel["step"] == "purchase", "users"].values[0]
overall_cvr    = round(total_buyers / total_visitors * 100, 2)

print(f"\n📊 OVERALL FUNNEL")
print(f"   Total Visitors  : {total_visitors:,}")
print(f"   Total Buyers    : {total_buyers:,}")
print(f"   Overall CVR     : {overall_cvr}%")

print(f"\n{'Step':<18} {'Users':>8} {'Conv%':>8} {'Drop%':>8}")
print("-" * 46)
prev = None
for _, row in funnel.iterrows():
    if prev:
        drop = round((1 - row["users"] / prev) * 100, 1)
        conv = round(row["users"] / prev * 100, 1)
    else:
        drop = 0.0
        conv = 100.0
    print(f"  {row['step']:<16} {int(row['users']):>8,} {conv:>7.1f}% {drop:>7.1f}%")
    prev = row["users"]

# ─── Identify biggest drop-off step ────────────────────────────────────────

drops = []
for i in range(1, len(funnel)):
    prev_u = funnel.iloc[i-1]["users"]
    curr_u = funnel.iloc[i]["users"]
    drops.append({
        "transition": f"{funnel.iloc[i-1]['step']} → {funnel.iloc[i]['step']}",
        "users_lost": int(prev_u - curr_u),
        "drop_rate":  round((1 - curr_u / prev_u) * 100, 1),
    })
drops_df = pd.DataFrame(drops).sort_values("drop_rate", ascending=False)

print(f"\n🚨 TOP DROP-OFF POINTS")
print(drops_df.to_string(index=False))
worst_step = drops_df.iloc[0]["transition"]
print(f"\n   ⚠️  Biggest leak : {worst_step} ({drops_df.iloc[0]['drop_rate']}% drop)")

# ─── 2. Segment Analysis ───────────────────────────────────────────────────

print("\n" + "=" * 55)
print("  SEGMENT ANALYSIS")
print("=" * 55)

def segment_cvr(seg_df, seg_col):
    visits    = seg_df[seg_df["step"] == "visit"][[seg_col, "users"]].rename(columns={"users": "visitors"})
    purchases = seg_df[seg_df["step"] == "purchase"][[seg_col, "users"]].rename(columns={"users": "purchasers"})
    merged    = visits.merge(purchases, on=seg_col, how="left").fillna(0)
    merged["cvr"] = (merged["purchasers"] / merged["visitors"] * 100).round(1)
    return merged.sort_values("cvr", ascending=False)

dev_cvr  = segment_cvr(dev_df,  "device")
chan_cvr = segment_cvr(chan_df, "channel")
age_cvr  = segment_cvr(age_df,  "age_group")
ctr_cvr  = segment_cvr(ctr_df,  "country")

print("\n📱 CVR by Device:")
print(dev_cvr.to_string(index=False))

print("\n📣 CVR by Acquisition Channel:")
print(chan_cvr.to_string(index=False))

print("\n👤 CVR by Age Group:")
print(age_cvr.to_string(index=False))

# ─── Root Cause (unchanged) ────────────────────────────────────────────────

mobile_cvr  = dev_cvr[dev_cvr["device"] == "mobile"]["cvr"].values[0]
desktop_cvr = dev_cvr[dev_cvr["device"] == "desktop"]["cvr"].values[0]
mobile_share= round(df[df["device"]=="mobile"]["user_id"].nunique() / df["user_id"].nunique() * 100, 1)

paid_cvr    = chan_cvr[chan_cvr["channel"] == "paid_ads"]["cvr"].values[0]
email_cvr   = chan_cvr[chan_cvr["channel"] == "email"]["cvr"].values[0]
paid_share  = round(df[df["channel"]=="paid_ads"]["user_id"].nunique() / df["user_id"].nunique() * 100, 1)

print("\n" + "=" * 55)
print("  ROOT CAUSE ANALYSIS")
print("=" * 55)

print(f"""
🔍 Finding 1 — Mobile UX Gap
   Mobile accounts for {mobile_share}% of traffic but converts at {mobile_cvr}%
   vs Desktop at {desktop_cvr}%.
   → Mobile checkout flow is likely causing friction.

🔍 Finding 2 — Paid Ad Quality
   Paid Ads bring {paid_share}% of traffic but CVR is only {paid_cvr}%
   vs Email at {email_cvr}%.
   → Audience mismatch causing early drop.
""")

# ─── Visualizations (UNCHANGED) ─────────────────────────────────────────────

sns.set_style("whitegrid")
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 130})

# (rest of your plotting code remains EXACTLY same — no changes needed)

conn.close()

print("\n🎉 Analysis complete. SQL integrated successfully.")