FlowLens — Funnel Intelligence Platform (v2.1)

A production-style analytics platform designed to identify conversion bottlenecks, analyze user behavior across funnel stages, and support data-driven decision-making through structured insights and visualization.

Live Application

(Add deployment link here)

Problem Statement

Digital businesses frequently experience significant user drop-off across the conversion funnel:

Visit → Signup → Add to Cart → Checkout → Purchase

Industry data suggests that a large percentage of users abandon the journey before completing a purchase, leading to substantial revenue loss. However, organizations often lack clarity on:

Where users drop off in the funnel
Which user segments underperform
What factors contribute to low conversion
Which actions can effectively improve outcomes
Solution Overview

FlowLens is an end-to-end funnel analytics system that:

Tracks user progression across funnel stages
Identifies critical drop-off points
Performs segment-level conversion analysis
Generates interpretable insights
Recommends business actions to improve conversion

The platform combines SQL-based data processing with Python-based analytics and visualization to simulate a real-world analytics workflow.

Key Features
Funnel Analysis Dashboard
Stage-wise user tracking from visit to purchase
Conversion rate and drop-off calculation at each step
Identification of the most critical leakage points
Segment-Level Analysis

Conversion Rate (CVR) analysis across:

Device type
Marketing channel
Age group
Geographic region

This enables comparison between high-performing and underperforming segments.

Insight Generation

The system identifies key behavioral patterns such as:

Conversion gaps between devices
Funnel bottlenecks (especially at checkout stage)
Low-performing acquisition channels

Insights are structured for business interpretation rather than raw reporting.

Recommendation Framework

Provides prioritized business actions based on observed patterns, such as:

Improving mobile checkout experience
Enabling guest checkout
Optimizing marketing channel allocation

Each recommendation is aligned with measurable business impact.

Data and Methodology
Dataset
Approximately 8,000 users
Over 17,000 event records
Time period: January to June 2024

The dataset simulates realistic user behavior, including:

Device usage patterns
Channel-based intent differences
Demographic variation in conversion
Sequential user journeys
Technical Approach
Data Processing

Raw event-level data is processed using SQL via SQLite.

Key operations include:

Aggregating stage-wise user counts
Computing conversion rates
Performing segment-level grouping
Analytics Layer

Python (Pandas and NumPy) is used for:

Funnel metric computation
Drop-off analysis
Segment comparison
Root-cause identification
Visualization

The project includes:

Funnel charts
Drop-off visualizations
Segment comparison plots
Heatmaps for behavioral analysis
Key Insights (Sample Output)
Overall conversion rate is below expected benchmarks
Highest drop-off occurs between Add to Cart and Checkout
Mobile users contribute a large share of traffic but convert less than desktop users
Email channel shows higher conversion efficiency compared to paid advertisements
Business Impact

The analysis supports actionable decisions such as:

Reducing checkout friction by enabling guest checkout
Improving mobile user experience to increase conversion
Optimizing marketing spend by focusing on high-performing channels
Recovering abandoned carts through targeted interventions
Technology Stack
Data Processing: SQL (SQLite), Pandas, NumPy
Visualization: Matplotlib, Seaborn
Application Layer: Streamlit
Data Generation: Synthetic behavioral simulation

Running the Project
pip install -r requirements.txt
streamlit run app.py
Learning Outcomes
Applied SQL for structured data extraction and aggregation
Translated raw event data into business metrics such as conversion rate and drop-off
Designed dashboards focused on decision-making
Built an end-to-end analytics workflow combining SQL and Python
Improved ability to communicate insights in a business context
Future Enhancements
Integration with real-time data sources
Cohort and retention analysis
A/B testing capabilities
Advanced user journey tracking
Secure deployment with authentication

Author

Prajakta
BSc Data Science