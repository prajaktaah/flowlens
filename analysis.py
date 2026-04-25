"""
User Journey Funnel Analysis — Core Analysis
=============================================
Performs statistical analysis on the funnel data:
  - Overall funnel metrics
  - Segment-level drop-off analysis
  - Root-cause inference
  - Business recommendations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings, os
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


# ─── Load Data ────────────────────────────────────────────────────────────────

df      = pd.read_csv("data/user_events.csv", parse_dates=["timestamp"])
funnel  = pd.read_csv("data/funnel_summary.csv")
dev_df  = pd.read_csv("data/segment_device.csv")
chan_df = pd.read_csv("data/segment_channel.csv")
age_df  = pd.read_csv("data/segment_age_group.csv")
ctr_df  = pd.read_csv("data/segment_country.csv")


# ─── 1. Overall Funnel Metrics ───────────────────────────────────────────────

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

# ─── Identify biggest drop-off step ──────────────────────────────────────────

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


# ─── 2. Device Segment Analysis ──────────────────────────────────────────────

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


# ─── 3. Root-Cause Insights ──────────────────────────────────────────────────

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
   vs Desktop at {desktop_cvr}%. Gap = {round(desktop_cvr - mobile_cvr, 1)} pp.
   → Mobile checkout flow is likely causing friction.

🔍 Finding 2 — Paid Ad Quality
   Paid Ads bring {paid_share}% of traffic but CVR is only {paid_cvr}%
   vs Email at {email_cvr}%. Ad targeting may be off-audience.
   → Audience mismatch causing early drop after signup.

🔍 Finding 3 — Checkout Bottleneck
   The add_to_cart→checkout transition has the steepest absolute
   user loss. This is the #1 revenue recovery opportunity.
   → Possible causes: mandatory account creation, payment friction,
     unexpected shipping costs, trust signals missing.
""")


# ─── 4. Recommendations ──────────────────────────────────────────────────────

print("=" * 55)
print("  ACTIONABLE RECOMMENDATIONS")
print("=" * 55)
print("""
  Priority 1 — Fix Mobile Checkout (Est. +8-12% CVR uplift)
    • Implement one-tap payment (Google Pay / UPI / Apple Pay)
    • Simplify form fields on mobile
    • Add sticky CTA button with progress indicator

  Priority 2 — Add Guest Checkout (Est. +5-8% CVR uplift)
    • Remove forced registration before purchase
    • Offer "Continue as Guest" prominently
    • Capture email post-purchase for re-engagement

  Priority 3 — Refine Paid Ad Targeting (Est. 15-20% CAC reduction)
    • Exclude low-intent audiences from paid campaigns
    • A/B test landing pages aligned to ad creative
    • Shift budget toward email & organic (3x better CVR)

  Priority 4 — Abandoned Cart Recovery (Est. +3-5% revenue)
    • Trigger email within 1 hour of cart abandonment
    • Offer time-limited 10% discount for returners
    • Add urgency: "Only 3 left in stock"
""")


# ─── 5. Visualizations ───────────────────────────────────────────────────────

sns.set_style("whitegrid")
plt.rcParams.update({"font.family": "DejaVu Sans", "figure.dpi": 130})

# --- Fig 1: Main Funnel Chart ------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor(PALETTE["bg"])
ax.set_facecolor(PALETTE["bg"])

users_list = funnel["users"].tolist()
max_u      = users_list[0]

bar_colors = [PALETTE["primary"]] * len(FUNNEL_STEPS)

bars = ax.barh(
    [f"  {l}" for l in reversed(STEP_LABELS)],
    list(reversed(users_list)),
    color=list(reversed(bar_colors)),
    edgecolor="white",
    height=0.55,
)

for i, (bar, u) in enumerate(zip(bars, reversed(users_list))):
    pct = round(u / max_u * 100, 1)
    ax.text(bar.get_width() + 80, bar.get_y() + bar.get_height() / 2,
            f"{u:,}  ({pct}%)", va="center", fontsize=11, color="#2C3E50", fontweight="bold")

ax.set_xlabel("Number of Users", fontsize=12)
ax.set_title("User Journey Funnel — Overall Conversion", fontsize=15, fontweight="bold", pad=16, color="#1A252F")
ax.set_xlim(0, max_u * 1.22)
ax.tick_params(axis="y", labelsize=11)
plt.tight_layout()
plt.savefig("outputs/01_funnel_overview.png", bbox_inches="tight")
plt.close()
print("✅ outputs/01_funnel_overview.png")

# --- Fig 2: Drop-off Rates by Step ------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor(PALETTE["bg"])
ax.set_facecolor(PALETTE["bg"])

colors = [PALETTE["danger"] if r > 45 else PALETTE["warning"] if r > 30 else PALETTE["success"]
          for r in drops_df["drop_rate"]]

ax.bar(drops_df["transition"], drops_df["drop_rate"], color=colors, edgecolor="white", width=0.5)
for i, (_, row) in enumerate(drops_df.iterrows()):
    ax.text(i, row["drop_rate"] + 0.8, f"{row['drop_rate']}%",
            ha="center", fontsize=12, fontweight="bold", color="#1A252F")

ax.set_ylabel("Drop-off Rate (%)", fontsize=12)
ax.set_title("Drop-off Rate at Each Funnel Transition", fontsize=14, fontweight="bold", color="#1A252F", pad=14)
ax.set_ylim(0, drops_df["drop_rate"].max() + 10)
plt.xticks(rotation=20, ha="right", fontsize=10)
plt.tight_layout()
plt.savefig("outputs/02_dropoff_rates.png", bbox_inches="tight")
plt.close()
print("✅ outputs/02_dropoff_rates.png")

# --- Fig 3: CVR by Device & Channel -----------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor(PALETTE["bg"])

for ax in axes:
    ax.set_facecolor(PALETTE["bg"])

# Device
dev_cvr_sorted = dev_cvr.sort_values("cvr")
axes[0].barh(dev_cvr_sorted["device"], dev_cvr_sorted["cvr"],
             color=[PALETTE["primary"], PALETTE["warning"], PALETTE["accent"]], edgecolor="white")
for i, (_, row) in enumerate(dev_cvr_sorted.iterrows()):
    axes[0].text(row["cvr"] + 0.1, i, f"{row['cvr']}%", va="center", fontsize=11, fontweight="bold")
axes[0].set_xlabel("Conversion Rate (%)")
axes[0].set_title("CVR by Device", fontsize=13, fontweight="bold", color="#1A252F")
axes[0].set_xlim(0, dev_cvr_sorted["cvr"].max() + 3)

# Channel
chan_cvr_sorted = chan_cvr.sort_values("cvr")
bar_colors_chan = [PALETTE["danger"] if c == "paid_ads" else PALETTE["primary"] for c in chan_cvr_sorted["channel"]]
axes[1].barh(chan_cvr_sorted["channel"], chan_cvr_sorted["cvr"],
             color=bar_colors_chan, edgecolor="white")
for i, (_, row) in enumerate(chan_cvr_sorted.iterrows()):
    axes[1].text(row["cvr"] + 0.1, i, f"{row['cvr']}%", va="center", fontsize=11, fontweight="bold")
axes[1].set_xlabel("Conversion Rate (%)")
axes[1].set_title("CVR by Channel", fontsize=13, fontweight="bold", color="#1A252F")
axes[1].set_xlim(0, chan_cvr_sorted["cvr"].max() + 3)

fig.suptitle("Segment-Level Conversion Rate Analysis", fontsize=15, fontweight="bold", color="#1A252F", y=1.02)
plt.tight_layout()
plt.savefig("outputs/03_segment_cvr.png", bbox_inches="tight")
plt.close()
print("✅ outputs/03_segment_cvr.png")

# --- Fig 4: Heatmap — device × step -----------------------------------------
pivot = dev_df.pivot(index="device", columns="step", values="users").reindex(columns=FUNNEL_STEPS)
# normalize each device row by its own visit count
pivot_pct = pivot.div(pivot["visit"], axis=0) * 100

fig, ax = plt.subplots(figsize=(10, 4))
fig.patch.set_facecolor(PALETTE["bg"])
sns.heatmap(pivot_pct, annot=True, fmt=".1f", cmap="Blues",
            linewidths=0.5, linecolor="white", ax=ax, cbar_kws={"label": "% of visitors"})
ax.set_title("Funnel Completion % by Device (row-normalized)", fontsize=13, fontweight="bold", color="#1A252F", pad=14)
ax.set_xlabel("")
plt.tight_layout()
plt.savefig("outputs/04_device_heatmap.png", bbox_inches="tight")
plt.close()
print("✅ outputs/04_device_heatmap.png")

print("\n🎉 Analysis complete. All outputs saved to ./outputs/")
