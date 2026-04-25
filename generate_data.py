"""
User Journey Funnel Analysis — Synthetic Data Generator
========================================================
Generates realistic user behavior data mimicking an e-commerce platform.
Incorporates real-world patterns: device bias, ad campaign quality variance,
time-of-day effects, and cohort-based dropout rates.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

np.random.seed(42)
random.seed(42)

# ─── Configuration ────────────────────────────────────────────────────────────

N_USERS = 8000
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 6, 30)

DEVICES    = ["mobile", "desktop", "tablet"]
DEVICE_W   = [0.60, 0.32, 0.08]           # mobile-heavy, realistic 2024

COUNTRIES  = ["India", "USA", "UK", "Germany", "Canada", "Australia", "Singapore"]
COUNTRY_W  = [0.35, 0.25, 0.12, 0.08, 0.07, 0.07, 0.06]

CHANNELS   = ["organic_search", "paid_ads", "social_media", "email", "direct", "referral"]
CHANNEL_W  = [0.30, 0.25, 0.20, 0.10, 0.10, 0.05]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
AGE_W      = [0.22, 0.35, 0.22, 0.13, 0.08]

FUNNEL_STEPS = ["visit", "signup", "add_to_cart", "checkout", "purchase"]

# Drop-off probabilities PER STEP (probability user proceeds to next step)
# These create the realistic funnel shape
BASE_CONVERSION = {
    "visit→signup":        0.62,
    "signup→add_to_cart":  0.52,
    "add_to_cart→checkout":0.40,
    "checkout→purchase":   0.55,
}

# Device multipliers on conversion rates
DEVICE_CONV_MULTIPLIER = {
    "mobile":  {"visit→signup": 0.82, "signup→add_to_cart": 0.78, "add_to_cart→checkout": 0.65, "checkout→purchase": 0.70},
    "desktop": {"visit→signup": 1.15, "signup→add_to_cart": 1.18, "add_to_cart→checkout": 1.25, "checkout→purchase": 1.20},
    "tablet":  {"visit→signup": 1.00, "signup→add_to_cart": 0.95, "add_to_cart→checkout": 0.95, "checkout→purchase": 1.00},
}

# Channel quality multipliers (paid ads = lower intent, email = high intent)
CHANNEL_CONV_MULTIPLIER = {
    "organic_search": {"visit→signup": 1.10, "signup→add_to_cart": 1.10, "add_to_cart→checkout": 1.10, "checkout→purchase": 1.10},
    "paid_ads":       {"visit→signup": 0.72, "signup→add_to_cart": 0.80, "add_to_cart→checkout": 0.85, "checkout→purchase": 0.90},
    "social_media":   {"visit→signup": 0.88, "signup→add_to_cart": 0.90, "add_to_cart→checkout": 0.88, "checkout→purchase": 0.92},
    "email":          {"visit→signup": 1.35, "signup→add_to_cart": 1.25, "add_to_cart→checkout": 1.20, "checkout→purchase": 1.15},
    "direct":         {"visit→signup": 1.20, "signup→add_to_cart": 1.15, "add_to_cart→checkout": 1.15, "checkout→purchase": 1.20},
    "referral":       {"visit→signup": 1.05, "signup→add_to_cart": 1.05, "add_to_cart→checkout": 1.05, "checkout→purchase": 1.05},
}

# Age group multipliers
AGE_CONV_MULTIPLIER = {
    "18-24": {"visit→signup": 1.05, "signup→add_to_cart": 0.88, "add_to_cart→checkout": 0.82, "checkout→purchase": 0.78},
    "25-34": {"visit→signup": 1.15, "signup→add_to_cart": 1.15, "add_to_cart→checkout": 1.12, "checkout→purchase": 1.15},
    "35-44": {"visit→signup": 1.08, "signup→add_to_cart": 1.10, "add_to_cart→checkout": 1.15, "checkout→purchase": 1.18},
    "45-54": {"visit→signup": 0.92, "signup→add_to_cart": 1.00, "add_to_cart→checkout": 1.05, "checkout→purchase": 1.10},
    "55+":   {"visit→signup": 0.75, "signup→add_to_cart": 0.85, "add_to_cart→checkout": 0.90, "checkout→purchase": 0.95},
}


# ─── Helper functions ─────────────────────────────────────────────────────────

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def get_conversion_prob(step_key, device, channel, age_group):
    base = BASE_CONVERSION[step_key]
    d_mult = DEVICE_CONV_MULTIPLIER[device][step_key]
    c_mult = CHANNEL_CONV_MULTIPLIER[channel][step_key]
    a_mult = AGE_CONV_MULTIPLIER[age_group][step_key]
    prob = base * d_mult * c_mult * a_mult
    # Add small random noise per user
    prob *= np.random.uniform(0.93, 1.07)
    return min(prob, 0.97)   # cap at 97%

def session_duration(step, device):
    """Realistic time spent on each step (seconds)"""
    base_times = {
        "visit": (30, 180),
        "signup": (60, 240),
        "add_to_cart": (120, 600),
        "checkout": (90, 480),
        "purchase": (20, 60),
    }
    lo, hi = base_times[step]
    if device == "mobile":
        lo, hi = int(lo * 0.8), int(hi * 0.8)
    return random.randint(lo, hi)

def page_views(step, device):
    """Pages viewed per step"""
    base = {"visit": (1, 4), "signup": (1, 2), "add_to_cart": (2, 8), "checkout": (2, 5), "purchase": (1, 2)}
    lo, hi = base[step]
    if device == "desktop":
        hi += 2
    return random.randint(lo, hi)


# ─── Main Generator ───────────────────────────────────────────────────────────

def generate_users():
    users = []
    for _ in range(N_USERS):
        device    = np.random.choice(DEVICES, p=DEVICE_W)
        channel   = np.random.choice(CHANNELS, p=CHANNEL_W)
        country   = np.random.choice(COUNTRIES, p=COUNTRY_W)
        age_group = np.random.choice(AGE_GROUPS, p=AGE_W)
        visit_ts  = random_date(START_DATE, END_DATE)
        users.append({
            "user_id":   str(uuid.uuid4())[:8].upper(),
            "device":    device,
            "channel":   channel,
            "country":   country,
            "age_group": age_group,
            "visit_ts":  visit_ts,
        })
    return users

def simulate_funnel(users):
    events = []
    step_keys = [
        "visit→signup",
        "signup→add_to_cart",
        "add_to_cart→checkout",
        "checkout→purchase",
    ]
    steps = FUNNEL_STEPS

    for u in users:
        ts = u["visit_ts"]
        current_step = 0   # always visits

        # Record visit event
        events.append({
            "user_id":        u["user_id"],
            "device":         u["device"],
            "channel":        u["channel"],
            "country":        u["country"],
            "age_group":      u["age_group"],
            "step":           steps[0],
            "step_order":     1,
            "timestamp":      ts,
            "session_sec":    session_duration(steps[0], u["device"]),
            "pages_viewed":   page_views(steps[0], u["device"]),
            "dropped_at":     None,
        })

        dropped = False
        for i, sk in enumerate(step_keys):
            prob = get_conversion_prob(sk, u["device"], u["channel"], u["age_group"])
            if random.random() < prob:
                current_step = i + 1
                ts = ts + timedelta(seconds=random.randint(60, 3600))
                events.append({
                    "user_id":      u["user_id"],
                    "device":       u["device"],
                    "channel":      u["channel"],
                    "country":      u["country"],
                    "age_group":    u["age_group"],
                    "step":         steps[i + 1],
                    "step_order":   i + 2,
                    "timestamp":    ts,
                    "session_sec":  session_duration(steps[i + 1], u["device"]),
                    "pages_viewed": page_views(steps[i + 1], u["device"]),
                    "dropped_at":   None,
                })
            else:
                # Mark where user dropped
                for ev in events:
                    if ev["user_id"] == u["user_id"]:
                        ev["dropped_at"] = sk.split("→")[1]   # dropped before this step
                dropped = True
                break

    df = pd.DataFrame(events)
    return df


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    print("🔄 Generating users...")
    users = generate_users()

    print("🔄 Simulating funnel journeys...")
    df = simulate_funnel(users)

    # Save raw events
    df.to_csv("data/user_events.csv", index=False)
    print(f"✅ user_events.csv  — {len(df):,} rows")

    # Funnel summary
    funnel = (
        df.groupby("step")["user_id"]
        .nunique()
        .reindex(FUNNEL_STEPS)
        .reset_index()
        .rename(columns={"user_id": "users"})
    )
    funnel["step_order"] = range(1, len(FUNNEL_STEPS) + 1)
    funnel["drop_from_prev"] = funnel["users"].diff(-1).fillna(0).astype(int)
    funnel["conv_from_prev"] = (funnel["users"] / funnel["users"].shift(1) * 100).round(1)
    funnel["conv_from_top"]  = (funnel["users"] / funnel["users"].iloc[0] * 100).round(1)
    funnel.to_csv("data/funnel_summary.csv", index=False)
    print(f"✅ funnel_summary.csv — {len(funnel)} steps")

    # Segment breakdown
    for seg in ["device", "channel", "age_group", "country"]:
        seg_df = (
            df.groupby([seg, "step"])["user_id"]
            .nunique()
            .reset_index()
            .rename(columns={"user_id": "users"})
        )
        seg_df.to_csv(f"data/segment_{seg}.csv", index=False)
        print(f"✅ segment_{seg}.csv")

    print("\n📦 All datasets saved to ./data/")
    print("\nFunnel Overview:")
    print(funnel[["step", "users", "conv_from_prev", "conv_from_top"]].to_string(index=False))
