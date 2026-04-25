"""
FlowLens — User Journey Funnel Intelligence  v2.0
Streamlit App | app.py
============================================================
Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FlowLens | Funnel Intelligence",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap');

html, body, [class*="css"]        { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header          { visibility: hidden; }

::-webkit-scrollbar               { width: 4px; }
::-webkit-scrollbar-track         { background: #09090F; }
::-webkit-scrollbar-thumb         { background: #2a2a3a; border-radius: 4px; }

section.main > div                { background: #09090F; }
[data-testid="stSidebar"]         { background: #0d0d15 !important; border-right: 1px solid rgba(255,255,255,0.06); }

.fl-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 1.6rem;
}
.fl-brand { display: flex; align-items: center; gap: 12px; }
.fl-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #4F8EF7 0%, #A78BFA 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; box-shadow: 0 0 20px rgba(79,142,247,0.35);
}
.fl-logo {
    font-family: 'Syne', sans-serif; font-size: 1.6rem; font-weight: 800;
    background: linear-gradient(90deg, #6FA8FF 0%, #C4B5FD 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}
.fl-tagline { font-size: 0.75rem; color: #6A6A7A; margin-top: 1px; }
.fl-pills { display: flex; gap: 8px; align-items: center; }
.pill { padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.8px; }
.pill-live {
    background: rgba(34,211,154,0.12); border: 1px solid rgba(34,211,154,0.3); color: #22D39A;
    animation: glow-green 2s ease-in-out infinite;
}
.pill-period { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #8A8A9A; }

@keyframes glow-green {
    0%,100% { box-shadow: 0 0 6px rgba(34,211,154,0.2); }
    50%      { box-shadow: 0 0 14px rgba(34,211,154,0.5); }
}

.alert-box {
    background: linear-gradient(90deg, rgba(255,71,87,0.12) 0%, rgba(255,71,87,0.03) 100%);
    border: 1px solid rgba(255,71,87,0.28); border-left: 3px solid #FF4757;
    border-radius: 10px; padding: 13px 18px; margin-bottom: 1.4rem;
    font-size: 0.84rem; color: #ccccdd; line-height: 1.55;
}
.alert-box strong { color: #FF6B7A; }

.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 1.6rem; }
.kpi-card {
    border-radius: 16px; padding: 18px 20px;
    border: 1px solid rgba(255,255,255,0.07);
    position: relative; overflow: hidden;
    transition: transform .2s, box-shadow .2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before {
    content:''; position:absolute; width:90px; height:90px;
    border-radius:50%; top:-20px; right:-20px;
    background: var(--blob); opacity:.18; filter:blur(22px);
}
.kpi-visitors  { background: linear-gradient(135deg,#0e1628,#111a30); --blob:#4F8EF7; box-shadow:0 0 0 1px rgba(79,142,247,.12),0 4px 24px rgba(0,0,0,.5); }
.kpi-buyers    { background: linear-gradient(135deg,#0e2218,#112a1e); --blob:#22D39A; box-shadow:0 0 0 1px rgba(34,211,154,.12),0 4px 24px rgba(0,0,0,.5); }
.kpi-cvr       { background: linear-gradient(135deg,#1e1228,#221430); --blob:#A78BFA; box-shadow:0 0 0 1px rgba(167,139,250,.12),0 4px 24px rgba(0,0,0,.5); }
.kpi-drop      { background: linear-gradient(135deg,#220f10,#2a1214); --blob:#FF4757; box-shadow:0 0 0 1px rgba(255,71,87,.12),0 4px 24px rgba(0,0,0,.5); }
.kpi-risk      { background: linear-gradient(135deg,#1e1a0a,#252010); --blob:#FFD93D; box-shadow:0 0 0 1px rgba(255,217,61,.12),0 4px 24px rgba(0,0,0,.5); }

.kpi-label { font-size:.68rem; text-transform:uppercase; letter-spacing:1.1px; color:#6A6A7A; margin-bottom:7px; }
.kpi-value { font-family:'Syne',sans-serif; font-size:1.85rem; font-weight:800; line-height:1; margin-bottom:5px; }
.kpi-sub   { font-size:.72rem; color:#6A6A7A; }
.kpi-badge { display:inline-flex; align-items:center; gap:3px; padding:2px 8px; border-radius:10px; font-size:.68rem; font-weight:700; }
.badge-up  { background:rgba(34,211,154,.15); color:#22D39A; }
.badge-dn  { background:rgba(255,71,87,.15); color:#FF4757; }

.c-blue{color:#6FA8FF} .c-green{color:#22D39A} .c-purple{color:#C4B5FD}
.c-red{color:#FF6B7A}  .c-yellow{color:#FFD93D}

.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(255,255,255,0.07),transparent); margin:1.4rem 0; }

.section-title {
    font-family:'Syne',sans-serif; font-size:.95rem; font-weight:700;
    color:#E8E8F0; margin-bottom:.9rem; display:flex; align-items:center; gap:8px;
}
.section-title span {
    font-family:'DM Sans',sans-serif; font-size:.68rem; font-weight:500; color:#6A6A7A;
    text-transform:uppercase; letter-spacing:.9px;
    background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);
    padding:2px 8px; border-radius:6px;
}

.insight-row {
    background:#13131e; border:1px solid rgba(255,255,255,0.06); border-radius:11px;
    padding:13px 15px; margin-bottom:9px; font-size:.82rem; color:#b8b8cc; line-height:1.55;
    transition: border-color .2s, background .2s;
}
.insight-row:hover { background:#16162a; border-color:rgba(255,255,255,0.1); }
.insight-row strong { color:#E8E8F0; }
.sev-h { border-left:3px solid #FF4757; }
.sev-m { border-left:3px solid #FFD93D; }
.sev-l { border-left:3px solid #22D39A; }

.reco-card {
    background:#13131e; border:1px solid rgba(255,255,255,0.06); border-radius:11px;
    padding:14px 16px; margin-bottom:9px; font-size:.82rem; color:#b8b8cc; line-height:1.5;
    transition: border-color .2s;
}
.reco-card:hover { border-color:rgba(255,255,255,0.1); }
.reco-card strong { color:#E8E8F0; }
.reco-card .impact { color:#22D39A; font-weight:600; }
.pr { font-weight:700; font-size:.68rem; text-transform:uppercase; letter-spacing:.9px; margin-bottom:4px; }
.pr1{color:#FF6B7A} .pr2{color:#FFD93D} .pr3{color:#6FA8FF}
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = Path(__file__).parent / "data"
    df      = pd.read_csv(base / "user_events.csv", parse_dates=["timestamp"])
    dev_df  = pd.read_csv(base / "segment_device.csv")
    chan_df = pd.read_csv(base / "segment_channel.csv")
    age_df  = pd.read_csv(base / "segment_age_group.csv")
    ctr_df  = pd.read_csv(base / "segment_country.csv")
    return df, dev_df, chan_df, age_df, ctr_df

df, dev_df, chan_df, age_df, ctr_df = load_data()

STEPS       = ["visit","signup","add_to_cart","checkout","purchase"]
STEP_LABELS = ["Visit","Sign Up","Add to Cart","Checkout","Purchase"]
C = dict(blue="#4F8EF7", green="#22D39A", red="#FF4757",
         yellow="#FFD93D", purple="#A78BFA", accent="#FF6B35")

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 6px 0'>
      <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:800;
           background:linear-gradient(90deg,#6FA8FF,#C4B5FD);
           -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
        🔭 FlowLens
      </div>
      <div style='font-size:.7rem;color:#5A5A7A;margin-top:2px;'>Funnel Intelligence v2.0</div>
    </div>
    <div style='height:1px;background:linear-gradient(90deg,rgba(79,142,247,.3),transparent);margin:10px 0 16px 0'></div>
    """, unsafe_allow_html=True)

    st.markdown("**🎛️ Filters**")
    sel_device  = st.multiselect("Device",   options=df["device"].unique().tolist(),  default=df["device"].unique().tolist())
    sel_channel = st.multiselect("Channel",  options=df["channel"].unique().tolist(), default=df["channel"].unique().tolist())
    sel_age     = st.multiselect("Age Group",options=sorted(df["age_group"].unique().tolist()), default=sorted(df["age_group"].unique().tolist()))
    sel_country = st.multiselect("Country",  options=df["country"].unique().tolist(), default=df["country"].unique().tolist())

    st.markdown("---")
    st.markdown("**📅 Date Range**")
    min_d, max_d = df["timestamp"].dt.date.min(), df["timestamp"].dt.date.max()
    date_range = st.date_input("", value=(min_d, max_d), min_value=min_d, max_value=max_d)

    st.markdown("---")
    st.markdown("**💰 Revenue Assumptions**")
    avg_order = st.slider("Avg Order Value (₹)", 500, 5000, 1500, 100)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:.7rem;color:#5A5A7A;line-height:1.6;'>
    8,000 synthetic users · 17,367 events<br>Jan–Jun 2024<br><br>
    <strong style='color:#4F8EF7'>BSc Data Science Portfolio</strong>
    </div>""", unsafe_allow_html=True)

# ─── Filter ───────────────────────────────────────────────────────────────────
mask = (df["device"].isin(sel_device) & df["channel"].isin(sel_channel) &
        df["age_group"].isin(sel_age) & df["country"].isin(sel_country))
if len(date_range) == 2:
    mask &= (df["timestamp"].dt.date >= date_range[0]) & (df["timestamp"].dt.date <= date_range[1])
fdf = df[mask].copy()

# ── Empty filter guard ────────────────────────────────────────────────────────
if fdf.empty:
    st.markdown("""
    <div style='text-align:center;padding:80px 20px;'>
      <div style='font-size:3rem;margin-bottom:16px;'>🔍</div>
      <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;color:#E8E8F0;margin-bottom:8px;'>
        No data matches your filters
      </div>
      <div style='font-size:.9rem;color:#6A6A7A;'>
        Try selecting at least one option in Device, Channel, Age Group, and Country.
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

def compute_funnel(data):
    rows = [{"step": s, "users": data[data["step"]==s]["user_id"].nunique()} for s in STEPS]
    f = pd.DataFrame(rows)
    f["pct"]       = (f["users"] / f["users"].iloc[0] * 100).round(1)
    f["conv_prev"] = (f["users"] / f["users"].shift(1) * 100).round(1)
    f["drop_prev"] = (100 - f["conv_prev"]).round(1)
    return f

funnelf        = compute_funnel(fdf)
total_vis      = int(funnelf.iloc[0]["users"])
total_buy      = int(funnelf.iloc[-1]["users"])
overall_cvr    = round(total_buy / max(total_vis,1) * 100, 2)

# Guard: if no data or all NaN, fall back to step index 2 (cart→checkout)
_drop_series   = funnelf["drop_prev"].iloc[1:]
_valid_drops   = _drop_series.dropna()
worst_idx      = int(_valid_drops.idxmax()) if not _valid_drops.empty else 2
worst_drop     = float(funnelf.loc[worst_idx, "drop_prev"]) if pd.notna(funnelf.loc[worst_idx, "drop_prev"]) else 0.0
worst_step     = funnelf.loc[worst_idx, "step"]
prev_step      = funnelf.loc[worst_idx-1, "step"]
users_lost_w   = int(funnelf.loc[worst_idx-1,"users"] - funnelf.loc[worst_idx,"users"])

def seg_cvr(data, col):
    v = data[data["step"]=="visit"].groupby(col)["user_id"].nunique().rename("visitors")
    p = data[data["step"]=="purchase"].groupby(col)["user_id"].nunique().rename("buyers")
    m = pd.concat([v,p], axis=1).fillna(0)
    m["cvr"] = (m["buyers"] / m["visitors"].replace(0, np.nan) * 100).round(1)
    return m

dev_cvr  = seg_cvr(fdf, "device")
chan_cvr = seg_cvr(fdf, "channel")
mob_cvr  = float(dev_cvr.loc["mobile","cvr"])  if "mobile"  in dev_cvr.index  else 0.0
desk_cvr = float(dev_cvr.loc["desktop","cvr"]) if "desktop" in dev_cvr.index  else 0.0
paid_cvr = float(chan_cvr.loc["paid_ads","cvr"]) if "paid_ads" in chan_cvr.index else 0.0
email_cvr= float(chan_cvr.loc["email","cvr"])    if "email"   in chan_cvr.index else 0.0
mob_share= round(fdf[fdf["device"]=="mobile"]["user_id"].nunique()/max(fdf["user_id"].nunique(),1)*100,1)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="fl-header">
  <div class="fl-brand">
    <div class="fl-icon">🔭</div>
    <div>
      <div class="fl-logo">FlowLens</div>
      <div class="fl-tagline">User Journey Funnel Intelligence Platform</div>
    </div>
  </div>
  <div class="fl-pills">
    <div class="pill pill-live">● LIVE</div>
    <div class="pill pill-period">Jan – Jun 2024 &nbsp;·&nbsp; E-Commerce</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="alert-box">
  ⚠️ <strong>Critical Drop-Off Detected:</strong>
  &nbsp;<strong>{worst_drop:.1f}%</strong> of users abandon at
  <strong>{prev_step.replace('_',' ').title()} → {worst_step.replace('_',' ').title()}</strong>
  &nbsp;·&nbsp; {users_lost_w:,} users lost
  &nbsp;·&nbsp; Est. revenue at risk: <strong>₹{int(users_lost_w * avg_order * overall_cvr/100):,}</strong>/month
  &nbsp;·&nbsp; Filters active: {len(sel_device)} devices · {len(sel_channel)} channels · {len(sel_age)} age groups
</div>
""", unsafe_allow_html=True)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
delta_cvr = round(overall_cvr - 14.2, 1)
badge_cvr = (f'<span class="kpi-badge badge-dn">↓ {abs(delta_cvr)}pp vs industry</span>'
             if delta_cvr < 0 else
             f'<span class="kpi-badge badge-up">↑ {delta_cvr}pp vs industry</span>')

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card kpi-visitors">
    <div class="kpi-label">Total Visitors</div>
    <div class="kpi-value c-blue">{total_vis:,}</div>
    <div class="kpi-sub">Jan – Jun 2024</div>
  </div>
  <div class="kpi-card kpi-buyers">
    <div class="kpi-label">Purchasers</div>
    <div class="kpi-value c-green">{total_buy:,}</div>
    <div class="kpi-sub">{round(total_buy/max(total_vis,1)*100,1)}% of visitors</div>
  </div>
  <div class="kpi-card kpi-cvr">
    <div class="kpi-label">Overall CVR</div>
    <div class="kpi-value c-purple">{overall_cvr}%</div>
    <div class="kpi-sub">{badge_cvr}</div>
  </div>
  <div class="kpi-card kpi-drop">
    <div class="kpi-label">Biggest Drop</div>
    <div class="kpi-value c-red">{worst_drop:.1f}%</div>
    <div class="kpi-sub">{prev_step.replace('_',' ').title()} → {worst_step.replace('_',' ').title()}</div>
  </div>
  <div class="kpi-card kpi-risk">
    <div class="kpi-label">Users Lost (Worst Step)</div>
    <div class="kpi-value c-yellow">{users_lost_w:,}</div>
    <div class="kpi-sub">₹{users_lost_w * avg_order // 1000}K revenue at risk</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Dashboard", "🧠  Insights & Recommendations", "🧮  Revenue Simulator"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:

    # ── Funnel chart + step table ─────────────────────────────────────────────
    st.markdown('<div class="section-title">📊 Conversion Funnel <span>Step-by-step</span></div>', unsafe_allow_html=True)

    fig_funnel = go.Figure(go.Funnel(
        y=STEP_LABELS,
        x=funnelf["users"].tolist(),
        textinfo="value+percent previous",
        textfont=dict(size=13, color="white", family="DM Sans"),
        marker=dict(
            color=[C["blue"],C["purple"],C["yellow"],C["accent"],C["green"]],
            line=dict(width=2, color="#09090F"),
        ),
        connector=dict(line=dict(color="rgba(255,255,255,0.06)", width=1)),
        opacity=0.92,
    ))
    fig_funnel.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=10,b=10), height=360,
        font=dict(family="DM Sans", size=12), showlegend=False,
    )
    st.plotly_chart(fig_funnel, use_container_width=True)

    tbl = []
    for i, row in funnelf.iterrows():
        tbl.append({
            "Step": row["step"].replace("_"," ").title(),
            "Users": f"{int(row['users']):,}",
            "% of Top": f"{row['pct']}%",
            "Conv. from Prev": f"{row['conv_prev']:.1f}%" if pd.notna(row["conv_prev"]) else "—",
            "Drop from Prev": f"{row['drop_prev']:.1f}%" if pd.notna(row["drop_prev"]) else "—",
        })
    st.dataframe(pd.DataFrame(tbl), use_container_width=True, hide_index=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Drop-off bars + Segment CVR ───────────────────────────────────────────
    col_d, col_s = st.columns(2, gap="large")

    with col_d:
        st.markdown('<div class="section-title">📉 Drop-off by Transition <span>Severity colored</span></div>', unsafe_allow_html=True)

        trans, rates, lost = [], [], []
        for i in range(1, len(funnelf)):
            pu = funnelf.iloc[i-1]["users"]; cu = funnelf.iloc[i]["users"]
            trans.append(f"{STEP_LABELS[i-1]} → {STEP_LABELS[i]}")
            rates.append(round((1 - cu/max(pu,1))*100, 1))
            lost.append(int(pu - cu))

        bar_c = [C["red"] if r>50 else C["yellow"] if r>35 else C["green"] for r in rates]

        fig_drop = go.Figure(go.Bar(
            x=trans, y=rates, marker_color=bar_c,
            marker_line_color="rgba(0,0,0,0.3)", marker_line_width=1,
            text=[f"{r}%" for r in rates], textposition="outside",
            textfont=dict(size=12, family="DM Sans"),
            customdata=lost,
            hovertemplate="<b>%{x}</b><br>Drop-off: <b>%{y}%</b><br>Users lost: <b>%{customdata:,}</b><extra></extra>",
        ))
        fig_drop.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=30,b=70), height=320,
            yaxis=dict(title="Drop-off %", range=[0, max(rates)+16], gridcolor="rgba(255,255,255,0.05)"),
            xaxis=dict(tickangle=-18, tickfont=dict(size=11)),
            font=dict(family="DM Sans", size=11), showlegend=False,
        )
        st.plotly_chart(fig_drop, use_container_width=True)

    with col_s:
        st.markdown('<div class="section-title">🔍 CVR by Segment <span>Switch view</span></div>', unsafe_allow_html=True)

        seg_choice = st.radio("", ["Device","Channel","Age Group","Country"],
                              horizontal=True, label_visibility="collapsed")
        sc = {"Device":"device","Channel":"channel","Age Group":"age_group","Country":"country"}[seg_choice]
        cvr_df = seg_cvr(fdf, sc).reset_index().sort_values("cvr")

        fig_seg = go.Figure(go.Bar(
            y=cvr_df[sc].astype(str), x=cvr_df["cvr"],
            orientation="h",
            marker=dict(
                color=cvr_df["cvr"].tolist(),
                colorscale=[[0,C["red"]],[0.45,C["yellow"]],[1,C["green"]]],
                showscale=True,
                colorbar=dict(title="CVR%", thickness=10, tickfont=dict(size=10)),
            ),
            text=[f"{v:.1f}%" for v in cvr_df["cvr"]], textposition="outside",
            textfont=dict(size=11, family="DM Sans"),
            hovertemplate="<b>%{y}</b><br>CVR: <b>%{x:.1f}%</b><extra></extra>",
        ))
        fig_seg.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=60,t=10,b=10), height=300,
            xaxis=dict(title="CVR %", gridcolor="rgba(255,255,255,0.05)"),
            font=dict(family="DM Sans", size=11), showlegend=False,
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Trend + Sankey ────────────────────────────────────────────────────────
    col_t, col_sk = st.columns(2, gap="large")

    with col_t:
        st.markdown('<div class="section-title">📈 Monthly CVR Trend <span>Jan – Jun 2024</span></div>', unsafe_allow_html=True)

        fdf["month"] = fdf["timestamp"].dt.to_period("M").astype(str)
        mv = fdf[fdf["step"]=="visit"].groupby("month")["user_id"].nunique().rename("visitors")
        mp = fdf[fdf["step"]=="purchase"].groupby("month")["user_id"].nunique().rename("buyers")
        monthly = pd.concat([mv,mp],axis=1).fillna(0)
        monthly["cvr"] = (monthly["buyers"]/monthly["visitors"].replace(0,np.nan)*100).round(2)
        monthly = monthly.reset_index()

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(
            x=monthly["month"], y=monthly["visitors"], name="Visitors", yaxis="y2",
            marker_color="rgba(79,142,247,0.18)",
            marker_line_color="rgba(79,142,247,0.4)", marker_line_width=1,
        ))
        fig_trend.add_trace(go.Scatter(
            x=monthly["month"], y=monthly["cvr"], name="Purchase CVR %",
            mode="lines+markers+text",
            line=dict(color=C["green"], width=3),
            marker=dict(size=9, color=C["green"], line=dict(color="#09090F", width=2)),
            fill="tozeroy", fillcolor="rgba(34,211,154,0.07)",
            text=[f"{v:.1f}%" for v in monthly["cvr"]],
            textposition="top center", textfont=dict(size=11, color=C["green"]),
        ))
        fig_trend.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10,r=10,t=10,b=10), height=300,
            yaxis=dict(title="CVR %", gridcolor="rgba(255,255,255,0.05)"),
            yaxis2=dict(title="Visitors", overlaying="y", side="right", showgrid=False),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=11)),
            font=dict(family="DM Sans", size=11),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col_sk:
        st.markdown('<div class="section-title">🌊 User Flow Sankey <span>Where users go</span></div>', unsafe_allow_html=True)

        labels = STEP_LABELS + [f"Dropped: {l}" for l in STEP_LABELS[1:]]
        source, target, value, lc = [], [], [], []
        node_colors = [C["blue"],C["purple"],C["yellow"],C["accent"],C["green"]] + ["rgba(255,71,87,0.7)"]*4

        for i in range(len(STEPS)-1):
            cu = int(funnelf.iloc[i]["users"]); nu = int(funnelf.iloc[i+1]["users"])
            source += [i,i]; target += [i+1, len(STEP_LABELS)+i]
            value  += [nu, cu-nu]
            lc     += ["rgba(79,142,247,0.3)","rgba(255,71,87,0.2)"]

        fig_sankey = go.Figure(go.Sankey(
            node=dict(pad=14, thickness=16,
                      line=dict(color="rgba(255,255,255,0.04)", width=0.5),
                      label=labels, color=node_colors,
                      hovertemplate="%{label}: %{value:,} users<extra></extra>"),
            link=dict(source=source, target=target, value=value, color=lc,
                      hovertemplate="Flow: %{value:,} users<extra></extra>"),
        ))
        fig_sankey.update_layout(
            template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", size=10, color="#8A8A9A"),
            margin=dict(l=10,r=10,t=10,b=10), height=300,
        )
        st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Raw Data Explorer ─────────────────────────────────────────────────────
    with st.expander("🔎 Raw Event Data Explorer"):
        st.markdown(f"Showing up to 500 rows from **{len(fdf):,}** filtered events")
        cols_show = ["user_id","device","channel","country","age_group","step","timestamp","session_sec","pages_viewed"]
        st.dataframe(fdf[cols_show].sort_values("timestamp", ascending=False).head(500),
                     use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — INSIGHTS & RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:

    ins_l, ins_r = st.columns(2, gap="large")

    with ins_l:
        st.markdown('<div class="section-title">🧠 Root-Cause Insights <span>Data-driven</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="insight-row sev-h">
  📱 <strong>Mobile UX Crisis</strong><br>
  {mob_share}% of traffic is mobile, but mobile CVR is only
  <strong class="c-red">{mob_cvr}%</strong> vs desktop
  <strong class="c-green">{desk_cvr}%</strong> —
  a <strong>{round(desk_cvr/max(mob_cvr,0.1),1)}× gap</strong>.
  Fixing mobile checkout is your highest-ROI action.
</div>
<div class="insight-row sev-h">
  🛒 <strong>Checkout Bottleneck — #1 Leak</strong><br>
  <strong class="c-red">{worst_drop:.1f}%</strong> of users drop at
  {prev_step.replace('_',' ').title()} → {worst_step.replace('_',' ').title()}.
  Forced sign-up, surprise costs, or payment friction are likely culprits.
</div>
<div class="insight-row sev-m">
  📣 <strong>Paid Ad Audience Mismatch</strong><br>
  Paid Ads CVR = <strong class="c-yellow">{paid_cvr}%</strong> vs Email
  <strong class="c-green">{email_cvr}%</strong>.
  Budget is flowing toward low-intent users who bounce early.
</div>
<div class="insight-row sev-l">
  🎯 <strong>Best Segments to Scale</strong><br>
  Email channel + age group 25–44 are your highest-value cohorts.
  Redirect budget here for maximum conversion lift.
</div>
<div class="insight-row sev-l">
  📅 <strong>Improving Trend</strong><br>
  CVR has grown from 7.8% in January to 11.3% in June — a positive signal.
  Sustaining this requires fixing the structural leaks above.
</div>
""", unsafe_allow_html=True)

    with ins_r:
        st.markdown('<div class="section-title">💡 Recommendations <span>Ranked by impact</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="reco-card">
  <div class="pr pr1">🔴 Priority 1 &nbsp;·&nbsp; Est. +8–12% CVR</div>
  <strong>Fix Mobile Checkout</strong><br>
  {mob_share}% of users are on mobile but converting at {mob_cvr}%.
  Add one-tap payment (UPI / Google Pay / Apple Pay), reduce form fields to 3,
  add a sticky progress CTA. Expected uplift: 8–12 percentage points.
</div>
<div class="reco-card">
  <div class="pr pr1">🔴 Priority 2 &nbsp;·&nbsp; Est. +5–8% CVR</div>
  <strong>Enable Guest Checkout</strong><br>
  Removing mandatory account creation before purchase is the single
  fastest fix. Capture the email post-purchase for re-engagement.
  A/B test: guest vs sign-up required.
</div>
<div class="reco-card">
  <div class="pr pr2">🟡 Priority 3 &nbsp;·&nbsp; Est. −15–20% CAC</div>
  <strong>Refine Paid Ad Targeting</strong><br>
  Email converts at {email_cvr}% — {round(email_cvr/max(paid_cvr,0.1),1)}× better than Paid Ads ({paid_cvr}%).
  Shift 30–40% of ad budget to email nurture sequences and
  lookalike audiences based on your best buyers (age 25–44, desktop).
</div>
<div class="reco-card">
  <div class="pr pr3">🔵 Priority 4 &nbsp;·&nbsp; Est. +3–5% revenue recovery</div>
  <strong>Abandoned Cart Recovery Email</strong><br>
  Trigger an automated email within 60 minutes of cart abandonment.
  Include a 10% time-limited discount and social proof (reviews).
  Industry average recovery rate: 5–15% of abandoned carts.
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Summary scorecard
    st.markdown('<div class="section-title">📋 Problem Summary <span>At a glance</span></div>', unsafe_allow_html=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1: st.metric("Industry Avg CVR", "14.2%", delta=f"{round(overall_cvr-14.2,1)}pp gap", delta_color="inverse")
    with sc2: st.metric("Mobile CVR Gap", f"{round(desk_cvr-mob_cvr,1)}pp", delta="Desktop vs Mobile", delta_color="inverse")
    with sc3: st.metric("Best Channel", "Email", delta=f"{email_cvr}% CVR")
    with sc4: st.metric("Worst Channel", "Paid Ads", delta=f"{paid_cvr}% CVR", delta_color="inverse")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — REVENUE SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:

    st.markdown('<div class="section-title">🧮 Revenue Impact Simulator <span>What if we fix it?</span></div>', unsafe_allow_html=True)
    st.markdown("<div style='font-size:.85rem;color:#8A8A9A;margin-bottom:20px;line-height:1.6;'>Model the revenue uplift from fixing the three biggest leaks. Adjust the sliders below — results update instantly. Use the <strong style='color:#E8E8F0'>Avg Order Value</strong> in the sidebar to match your business.</div>", unsafe_allow_html=True)

    sim1, sim2, sim3 = st.columns(3)
    with sim1:
        checkout_lift = st.slider("Checkout CVR improvement (%pts)", 0, 25, 10,
            help="If checkout friction is fixed, by how many percentage points does CVR improve?")
    with sim2:
        mobile_lift = st.slider("Mobile CVR improvement (%pts)", 0, 15, 5,
            help="After improving mobile UX, how much does mobile CVR increase?")
    with sim3:
        ad_shift = st.slider("Budget shifted: Ads → Email (%)", 0, 80, 30,
            help="Email converts 5× better. Moving ad budget here recovers significant revenue.")

    cart_users_base    = int(funnelf[funnelf["step"]=="add_to_cart"]["users"].values[0])
    purchase_base      = int(funnelf[funnelf["step"]=="purchase"]["users"].values[0])
    checkout_conv_base = purchase_base / max(cart_users_base, 1)
    checkout_conv_new  = min(checkout_conv_base + checkout_lift/100, 0.97)
    extra_checkout     = max(int(cart_users_base * checkout_conv_new) - purchase_base, 0)

    mobile_users = int(fdf[fdf["device"]=="mobile"]["user_id"].nunique())
    extra_mobile = max(int(mobile_users * min(mob_cvr/100 + mobile_lift/100, 0.97)) - int(mobile_users * mob_cvr/100), 0)

    paid_users   = int(fdf[fdf["channel"]=="paid_ads"]["user_id"].nunique())
    extra_email  = max(int(paid_users * ad_shift/100 * (email_cvr - paid_cvr)/100), 0)

    extra_total  = extra_checkout + extra_mobile + extra_email
    extra_rev    = extra_total * avg_order
    new_cvr_sim  = round((purchase_base + extra_total) / max(total_vis,1) * 100, 2)

    st.markdown('<br>', unsafe_allow_html=True)
    r1, r2, r3, r4 = st.columns(4)
    with r1: st.metric("Extra Buyers (6mo)",  f"+{extra_total:,}",  delta="from baseline")
    with r2: st.metric("Extra Revenue (6mo)", f"₹{extra_rev:,.0f}", delta="incremental")
    with r3: st.metric("New Overall CVR",      f"{max(new_cvr_sim, overall_cvr):.2f}%", delta=f"+{max(new_cvr_sim-overall_cvr,0):.2f}pp")
    with r4: st.metric("Revenue Multiplier",   f"{round(extra_rev/max(avg_order*100,1),1)}×", delta="vs current")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Breakdown bar chart
    st.markdown('<div class="section-title">📊 Uplift Breakdown <span>By fix</span></div>', unsafe_allow_html=True)
    fig_sim = go.Figure(go.Bar(
        x=["Fix Mobile Checkout", "Improve Mobile UX", "Shift Ads → Email"],
        y=[extra_checkout * avg_order, extra_mobile * avg_order, extra_email * avg_order],
        marker_color=[C["red"], C["yellow"], C["green"]],
        text=[f"₹{v:,.0f}" for v in [extra_checkout*avg_order, extra_mobile*avg_order, extra_email*avg_order]],
        textposition="outside",
        textfont=dict(size=12, family="DM Sans"),
    ))
    fig_sim.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=30,b=10), height=320,
        yaxis=dict(title="Extra Revenue (₹)", gridcolor="rgba(255,255,255,0.05)"),
        font=dict(family="DM Sans", size=11), showlegend=False,
    )
    st.plotly_chart(fig_sim, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center;color:#4A4A5A;font-size:.72rem;
     padding:1.8rem 0 1rem 0;border-top:1px solid rgba(255,255,255,0.05);margin-top:1rem;'>
  🔭 <strong style='color:#4F8EF7'>FlowLens v2.0</strong>
  &nbsp;·&nbsp; User Journey Funnel Intelligence
  &nbsp;·&nbsp; Python · Pandas · Plotly · Streamlit
  &nbsp;·&nbsp; <strong style='color:#A78BFA'>BSc Data Science Portfolio Project</strong>
</div>
""", unsafe_allow_html=True)