# 🔭 FlowLens — Funnel Intelligence Platform (v2.0)

> **A production-style analytics dashboard that detects revenue leaks, explains why users drop, and simulates how to recover lost revenue.**

---

## 🌐 Live App

👉 *(Add your deployed link here after using Streamlit Cloud)*

---

## 🧩 Problem Statement

Every digital business faces the same silent issue:

> Users visit → explore → add to cart → and then disappear.

Globally, **~70% of carts are abandoned**, leading to massive revenue loss.
However, most teams lack clarity on:

* Where users drop off
* Which segments are underperforming
* Why conversion fails
* What actions will actually improve revenue

---

## 🎯 Solution — FlowLens

FlowLens is an **end-to-end funnel intelligence platform** that:

* Tracks user movement across funnel stages
* Identifies **critical drop-off points**
* Analyzes **conversion by segment**
* Generates **data-driven insights**
* Simulates **revenue impact of improvements**

---

## ⚡ Key Features

### 📊 Interactive Funnel Dashboard

* Step-by-step conversion analysis (Visit → Purchase)
* Visual funnel + drop-off severity tracking
* Real-time filtering (device, channel, age, country)

### 🔍 Segment Intelligence

* Conversion Rate (CVR) by:

  * Device
  * Marketing Channel
  * Age Group
  * Country
* Highlights high-performing vs leaking segments

### 🧠 Automated Insights Engine

* Detects:

  * Mobile vs Desktop performance gaps
  * Checkout bottlenecks
  * Low-quality traffic sources
* Presents **human-readable insights**

### 💡 Recommendation System

* Prioritized actions ranked by:

  * Impact on CVR
  * Business ROI
* Example:

  * Fix mobile checkout
  * Enable guest checkout
  * Shift ad budget → email

### 🧮 Revenue Impact Simulator

* Models revenue uplift from:

  * Checkout improvements
  * Mobile UX fixes
  * Marketing reallocation
* Outputs:

  * Extra buyers
  * Incremental revenue
  * New CVR

### 🌊 User Flow Sankey

* Visualizes:

  * Where users continue
  * Where they drop

---

## 📊 Dataset

* **8,000 synthetic users**
* **17,000+ events**
* Timeframe: Jan–Jun 2024

### Why synthetic?

The dataset is designed to **mimic real-world behavior**, including:

* Device bias (mobile-heavy traffic, lower CVR)
* Channel intent differences (email vs paid ads)
* Age-based conversion patterns
* Realistic session timelines

---

## 🧠 Key Insights (Example Output)

* **Overall CVR:** ~9.6% (vs 14.2% industry benchmark)
* **Biggest Drop-Off:** Cart → Checkout (~57%)
* **Mobile CVR:** ~3% vs Desktop ~22%
* **Best Channel:** Email (~20% CVR)
* **Worst Channel:** Paid Ads (~4% CVR)

---

## 💼 Business Impact

FlowLens doesn’t just analyze — it **drives decisions**:

| Problem           | Action                | Impact          |
| ----------------- | --------------------- | --------------- |
| Checkout friction | Enable guest checkout | +5–8% CVR       |
| Mobile drop-offs  | Improve UX + payments | +8–12% CVR      |
| Poor ad targeting | Shift to email        | ↓ CAC by 15–20% |
| Abandoned carts   | Recovery emails       | +3–5% revenue   |

---

## 🛠️ Tech Stack

| Layer              | Tools                           |
| ------------------ | ------------------------------- |
| Frontend + Backend | Streamlit                       |
| Data Processing    | Pandas, NumPy                   |
| Visualization      | Plotly                          |
| Data Design        | Synthetic behavioral simulation |
| Styling            | Custom CSS inside Streamlit     |

---

## 📁 Project Structure

```
flowlens/
│
├── app.py                     # Main Streamlit application
├── data/
│   ├── user_events.csv
│   ├── segment_device.csv
│   ├── segment_channel.csv
│   ├── segment_age_group.csv
│   └── segment_country.csv
│
├── generate_data.py           # Synthetic data generator
├── analysis.py                # Offline analysis scripts
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧠 What I Learned

* Translating raw event data into **business metrics (CVR, drop-off)**
* Designing **decision-focused dashboards**
* Building **interactive analytics apps with Streamlit**
* Thinking like a **Product/Data Analyst**, not just a coder

---

## 🚀 Future Improvements

* Real-time data integration (SQL / APIs)
* Cohort retention analysis
* A/B testing module
* User-level journey tracking
* Deployment with authentication

---

## 💼 Interview Summary

> Built a funnel intelligence platform analyzing 8,000 users across a 5-step journey. Identified a 57% checkout drop-off and a 7× mobile vs desktop conversion gap. Delivered actionable recommendations and a simulation engine to estimate revenue uplift.

---

## 👤 Author

**Prajakta**
BSc Data Science

---

## ⭐ If you found this useful

Star the repo ⭐ and feel free to connect!
