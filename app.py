# ─────────────────────────────────────────────────────────────
# app.py — Athlete Recovery Dashboard
# Ishant Shah — CS32 Final Project
#
# Run with:   streamlit run app.py
#
# Reads from: recovery_log.csv  (created by injury_risk_recovery.py)
#             sport_profiles.csv (sport-specific thresholds)
# ─────────────────────────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import csv

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Recovery Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Barlow+Condensed:wght@300;400;600;700;800&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0d0f14;
    color: #e8eaf0;
}
.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1300px;
}
.dash-header {
    border-bottom: 1px solid #2a2d38;
    padding-bottom: 1.4rem;
    margin-bottom: 2rem;
}
.dash-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 800;
    font-size: 3rem;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin: 0 0 0.2rem 0;
    line-height: 1;
}
.dash-header p {
    font-size: 0.95rem;
    color: #6b7280;
    margin: 0;
    font-weight: 300;
}
.accent { color: #4ade80; }

.metric-card {
    background: #13161e;
    border: 1px solid #1f2330;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #4ade80, #22d3ee);
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    line-height: 1;
    color: #ffffff;
}
.metric-sub {
    font-size: 0.78rem;
    color: #6b7280;
    margin-top: 0.3rem;
}

.risk-HIGH   { color: #f87171; font-weight: 700; }
.risk-MEDIUM { color: #fbbf24; font-weight: 700; }
.risk-LOW    { color: #4ade80; font-weight: 700; }
.risk-value  {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
}

.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #e8eaf0;
    text-transform: uppercase;
    margin: 2.2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1f2330;
}

.pill-warn {
    display: inline-block;
    background: rgba(248,113,113,0.12);
    border: 1px solid rgba(248,113,113,0.3);
    color: #f87171;
    border-radius: 6px;
    padding: 0.45rem 0.9rem;
    font-size: 0.85rem;
    margin: 0.25rem 0;
    width: 100%;
}
.pill-rec {
    display: inline-block;
    background: rgba(74,222,128,0.10);
    border: 1px solid rgba(74,222,128,0.25);
    color: #4ade80;
    border-radius: 6px;
    padding: 0.45rem 0.9rem;
    font-size: 0.85rem;
    margin: 0.25rem 0;
    width: 100%;
}
.pill-ok {
    display: inline-block;
    background: rgba(34,211,238,0.10);
    border: 1px solid rgba(34,211,238,0.25);
    color: #22d3ee;
    border-radius: 6px;
    padding: 0.45rem 0.9rem;
    font-size: 0.85rem;
    margin: 0.25rem 0;
    width: 100%;
}

.stDataFrame { border-radius: 8px; overflow: hidden; }
thead tr th {
    background-color: #1a1d27 !important;
    color: #9ca3af !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
tbody tr td { font-size: 0.88rem !important; }
tbody tr:hover td { background-color: #1a1d27 !important; }

.no-data {
    text-align: center;
    padding: 5rem 2rem;
    color: #4b5563;
}
.no-data h2 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #374151;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SPORT PROFILE LOADER
# Reads thresholds from sport_profiles.csv so warnings and
# recommendations match the same targets as the CLI tool.
# ─────────────────────────────────────────────────────────────

PROFILES_FILE = "sport_profiles.csv"

DEFAULT_PROFILE = {
    "sport": "general",
    "sleep_target": 8.0,
    "hydration_target": 3.0,
    "protein_target": 120.0,
    "max_safe_intensity": 8,
    "max_safe_hr": 185.0,
}


def load_sport_profile_for_dashboard(sport_type):
    """
    Look up sport-specific thresholds from sport_profiles.csv.
    Falls back to the 'general' row if the sport isn't listed.
    """
    if not os.path.exists(PROFILES_FILE):
        return DEFAULT_PROFILE.copy()

    sport_lower = str(sport_type).strip().lower()
    general_row = None

    with open(PROFILES_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["sport"].strip().lower() == sport_lower:
                return {
                    "sport": row["sport"],
                    "sleep_target": float(row["sleep_target"]),
                    "hydration_target": float(row["hydration_target"]),
                    "protein_target": float(row["protein_target"]),
                    "max_safe_intensity": int(row["max_safe_intensity"]),
                    "max_safe_hr": float(row["max_safe_hr"]),
                }
            if row["sport"].strip().lower() == "general":
                general_row = row

    if general_row:
        return {
            "sport": "general",
            "sleep_target": float(general_row["sleep_target"]),
            "hydration_target": float(general_row["hydration_target"]),
            "protein_target": float(general_row["protein_target"]),
            "max_safe_intensity": int(general_row["max_safe_intensity"]),
            "max_safe_hr": float(general_row["max_safe_hr"]),
        }

    return DEFAULT_PROFILE.copy()


# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────

CSV_FILE = "recovery_log.csv"


def load_data():
    """
    Read the CSV created by injury_risk_recovery.py.
    Returns a cleaned DataFrame, or None if the file is missing / empty.
    """
    if not os.path.exists(CSV_FILE):
        return None

    df = pd.read_csv(CSV_FILE)
    if df.empty:
        return None

    numeric_cols = [
        "sleep_hours", "hydration_liters", "protein_grams",
        "soreness_level", "training_intensity",
        "avg_heart_rate", "max_heart_rate",
        "recovery_score", "day_number"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.sort_values("day_number").reset_index(drop=True)
    return df


# ─────────────────────────────────────────────────────────────
# WARNINGS & RECOMMENDATIONS
# Uses sport-specific thresholds from sport_profiles.csv and
# gives specific numbers (same logic as the CLI tool).
# ─────────────────────────────────────────────────────────────

def derive_warnings(row, profile):
    """Return warning strings using sport-specific thresholds."""
    w = []
    supplement_use = str(row.get("supplement_use", "no")).lower()

    if row["sleep_hours"] < profile["sleep_target"] - 2:
        w.append("Low sleep may reduce recovery and increase injury risk.")
    if row["hydration_liters"] < profile["hydration_target"] * 0.67:
        w.append("Low hydration may negatively affect performance and recovery.")
    if row["protein_grams"] < profile["protein_target"] * 0.5 and supplement_use != "yes":
        w.append("Low protein intake may limit muscle recovery.")
    if row["soreness_level"] >= 7:
        w.append("High soreness may be a sign your body needs more recovery.")
    if row["training_intensity"] >= profile["max_safe_intensity"]:
        w.append("Very high training intensity can increase strain on the body.")

    max_hr = float(row.get("max_heart_rate", 0) or 0)
    avg_hr = float(row.get("avg_heart_rate", 0) or 0)
    if max_hr > profile["max_safe_hr"]:
        w.append(
            f"Max heart rate of {int(max_hr)} bpm exceeded your sport's safe limit "
            f"of {int(profile['max_safe_hr'])} bpm — signs of overexertion."
        )
    if avg_hr > profile["max_safe_hr"] * 0.85:
        w.append(
            f"Average heart rate of {int(avg_hr)} bpm suggests sustained "
            f"high-intensity effort — monitor fatigue closely."
        )
    if row["sleep_hours"] < profile["sleep_target"] - 2 and row["training_intensity"] >= profile["max_safe_intensity"]:
        w.append("High intensity combined with low sleep is a risky recovery pattern.")
    if row["soreness_level"] >= 7 and row["training_intensity"] >= 7:
        w.append("High soreness plus hard training may increase injury risk.")

    return w


def derive_recommendations(row, profile):
    """Return recommendations with specific numbers and sport-aware targets."""
    r = []
    sport = profile["sport"]
    supplement_use = str(row.get("supplement_use", "no")).lower()

    if row["sleep_hours"] < profile["sleep_target"]:
        extra = round(profile["sleep_target"] - row["sleep_hours"], 1)
        r.append(f"Try sleeping {extra} more hours to reach the {sport} target of {profile['sleep_target']}h.")

    if row["hydration_liters"] < profile["hydration_target"]:
        extra = round(profile["hydration_target"] - row["hydration_liters"], 1)
        r.append(f"Drink {extra} more liters of water to reach your {sport} target of {profile['hydration_target']}L.")

    effective_protein = row["protein_grams"] * 1.1 if supplement_use == "yes" else row["protein_grams"]
    if effective_protein < profile["protein_target"]:
        extra = round(profile["protein_target"] - row["protein_grams"])
        note = " (supplements help, but whole food sources are more effective)" if supplement_use == "yes" else ""
        r.append(
            f"Eat {extra} more grams of protein to reach your {sport} target "
            f"of {int(profile['protein_target'])}g{note}."
        )

    if row["soreness_level"] >= 7:
        r.append("Consider lighter training, mobility work, or an extra recovery day.")

    if row["training_intensity"] >= profile["max_safe_intensity"]:
        r.append(
            f"Monitor hard training days carefully — {sport} athletes should avoid "
            f"stacking too many intensity {profile['max_safe_intensity']}+ sessions in a row."
        )

    if not r:
        r.append("Your habits look balanced today. Keep maintaining this pattern.")
    return r


# ─────────────────────────────────────────────────────────────
# BASELINE COMPUTATION
# Calculates rolling 7-day averages, all-time stats, and
# a consecutive LOW-risk streak count.
# ─────────────────────────────────────────────────────────────

def compute_baselines(df):
    """
    Returns (baselines dict, df with rolling_avg column added).
    baselines keys: recovery_score, sleep_hours, hydration_liters,
                    protein_grams (each with last7_mean, all_mean, all_min, all_max),
                    plus low_risk_streak.
    """
    df = df.copy()
    df["rolling_avg"] = df["recovery_score"].rolling(7, min_periods=1).mean().round(1)

    metrics = ["recovery_score", "sleep_hours", "hydration_liters", "protein_grams"]
    last7 = df.tail(7)
    baselines = {}
    for m in metrics:
        baselines[m] = {
            "last7_mean": round(last7[m].mean(), 1),
            "all_mean":   round(df[m].mean(), 1),
            "all_min":    round(df[m].min(), 1),
            "all_max":    round(df[m].max(), 1),
        }

    # Consecutive LOW-risk session streak
    streak = 0
    for val in reversed(df["injury_risk"].tolist()):
        if str(val) == "LOW":
            streak += 1
        else:
            break
    baselines["low_risk_streak"] = streak

    return baselines, df


# ─────────────────────────────────────────────────────────────
# PATTERN DETECTION
# Scans the full session history for multi-day patterns that
# a single-session view would miss.
# ─────────────────────────────────────────────────────────────

def detect_patterns(df, profile):
    """Return a list of multi-day pattern strings detected across all sessions."""
    patterns = []
    if len(df) < 2:
        return patterns

    soreness_vals  = df["soreness_level"].tolist()
    intensity_vals = df["training_intensity"].tolist()
    sleep_vals     = df["sleep_hours"].tolist()
    score_vals     = df["recovery_score"].tolist()

    # Consecutive high soreness
    streak = 0
    for v in reversed(soreness_vals):
        if v >= 7:
            streak += 1
        else:
            break
    if streak >= 2:
        patterns.append(
            f"High soreness (≥7) for {streak} consecutive sessions — "
            f"your body may need a recovery day."
        )

    # Consecutive high-intensity sessions
    streak = 0
    for v in reversed(intensity_vals):
        if v >= profile["max_safe_intensity"]:
            streak += 1
        else:
            break
    if streak >= 2:
        patterns.append(
            f"High training intensity (≥{profile['max_safe_intensity']}) for "
            f"{streak} consecutive sessions — overtraining risk."
        )

    # Recovery score consistently below all-time average
    if len(df) >= 4:
        all_mean = df["recovery_score"].mean()
        last3 = score_vals[-3:]
        if all(s < all_mean for s in last3):
            patterns.append(
                f"Recovery score has been below your all-time average "
                f"({all_mean:.0f}) for the last 3 sessions — review your habits."
            )

    # Improving trend over last 3 sessions
    if len(df) >= 4:
        last3 = score_vals[-3:]
        if last3[2] > last3[1] > last3[0]:
            patterns.append(
                "Recovery score is trending upward over the last 3 sessions — keep it up!"
            )

    # Chronic low sleep
    streak = 0
    for v in reversed(sleep_vals):
        if v < profile["sleep_target"] - 1:
            streak += 1
        else:
            break
    if streak >= 3:
        patterns.append(
            f"Sleep has been below {profile['sleep_target'] - 1}h for "
            f"{streak} consecutive sessions — sleep debt increases injury risk."
        )

    return patterns


# ─────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────

CHART_BG   = "#0d0f14"
PAPER_BG   = "#13161e"
GRID_COLOR = "#1f2330"
FONT_COLOR = "#9ca3af"

PLOTLY_LAYOUT = dict(
    plot_bgcolor=CHART_BG,
    paper_bgcolor=PAPER_BG,
    font=dict(color=FONT_COLOR, family="Barlow, sans-serif", size=12),
    margin=dict(l=12, r=12, t=36, b=12),
    xaxis=dict(showgrid=False, color=FONT_COLOR, zeroline=False),
    yaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR, zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
)


def chart_recovery_over_time(df):
    """Line chart — daily recovery score + 7-day rolling average baseline."""
    fig = go.Figure()

    fig.add_hrect(y0=0,  y1=45,  fillcolor="rgba(248,113,113,0.06)", line_width=0)
    fig.add_hrect(y0=45, y1=70,  fillcolor="rgba(251,191,36,0.05)",  line_width=0)
    fig.add_hrect(y0=70, y1=105, fillcolor="rgba(74,222,128,0.05)",  line_width=0)

    fig.add_trace(go.Scatter(
        x=df["day_number"], y=df["recovery_score"],
        mode="lines+markers",
        name="Daily Score",
        line=dict(color="#4ade80", width=2.5),
        marker=dict(size=7, color="#4ade80", line=dict(color="#0d0f14", width=1.5)),
        hovertemplate="Day %{x}<br>Score: %{y}<extra></extra>"
    ))

    # 7-day rolling average — the athlete's evolving baseline
    fig.add_trace(go.Scatter(
        x=df["day_number"], y=df["rolling_avg"],
        mode="lines",
        name="7-Day Avg (Baseline)",
        line=dict(color="#a78bfa", width=2, dash="dot"),
        hovertemplate="Day %{x}<br>7-Day Avg: %{y:.1f}<extra></extra>"
    ))

    fig.add_hline(y=70, line_dash="dash", line_color="#fbbf24", line_width=1,
                  annotation_text="Medium risk", annotation_position="bottom right",
                  annotation_font_color="#fbbf24", annotation_font_size=10)
    fig.add_hline(y=45, line_dash="dash", line_color="#f87171", line_width=1,
                  annotation_text="High risk", annotation_position="bottom right",
                  annotation_font_color="#f87171", annotation_font_size=10)

    fig.update_layout(**PLOTLY_LAYOUT, title="Recovery Score Over Time")
    fig.update_yaxes(range=[0, 105])
    return fig


def chart_sleep_over_time(df):
    """Bar chart — sleep hours per session."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["day_number"], y=df["sleep_hours"],
        name="Sleep Hours",
        marker_color="#22d3ee",
        hovertemplate="Day %{x}<br>Sleep: %{y}h<extra></extra>"
    ))
    fig.add_hline(y=8, line_dash="dot", line_color="#4ade80", line_width=1,
                  annotation_text="Ideal (8h)", annotation_position="bottom right",
                  annotation_font_color="#4ade80", annotation_font_size=10)
    fig.update_layout(**PLOTLY_LAYOUT, title="Sleep Hours Per Session")
    fig.update_yaxes(range=[0, 12])
    return fig


def chart_soreness_vs_intensity(df):
    """Scatter — soreness vs intensity, coloured by recovery score."""
    fig = px.scatter(
        df,
        x="training_intensity",
        y="soreness_level",
        color="recovery_score",
        color_continuous_scale=["#f87171", "#fbbf24", "#4ade80"],
        range_color=[0, 100],
        size_max=14,
        hover_data={"day_number": True, "recovery_score": True},
        labels={
            "training_intensity": "Training Intensity",
            "soreness_level": "Soreness Level",
            "recovery_score": "Recovery Score",
        },
        title="Soreness vs Training Intensity",
    )
    fig.add_shape(type="rect", x0=7, y0=7, x1=10, y1=10,
                  fillcolor="rgba(248,113,113,0.08)",
                  line=dict(color="#f87171", dash="dot", width=1))
    fig.add_annotation(x=8.5, y=9.5, text="High-risk zone",
                       showarrow=False, font=dict(color="#f87171", size=10))
    fig.update_traces(marker=dict(size=10, line=dict(color="#0d0f14", width=1)))
    fig.update_layout(**PLOTLY_LAYOUT,
                      coloraxis_colorbar=dict(title="Recovery", tickfont=dict(color=FONT_COLOR)))
    return fig


def chart_hydration_protein(df):
    """Dual-axis line chart — hydration and protein together."""
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=df["day_number"], y=df["hydration_liters"],
        name="Hydration (L)", mode="lines+markers",
        line=dict(color="#38bdf8", width=2),
        marker=dict(size=6),
        hovertemplate="Day %{x}<br>Hydration: %{y}L<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=df["day_number"], y=df["protein_grams"],
        name="Protein (g)", mode="lines+markers",
        line=dict(color="#a78bfa", width=2, dash="dot"),
        marker=dict(size=6),
        hovertemplate="Day %{x}<br>Protein: %{y}g<extra></extra>"
    ), secondary_y=True)
    fig.update_layout(**PLOTLY_LAYOUT, title="Hydration & Protein Trends")
    fig.update_yaxes(title_text="Hydration (L)", secondary_y=False,
                     gridcolor=GRID_COLOR, color=FONT_COLOR)
    fig.update_yaxes(title_text="Protein (g)", secondary_y=True,
                     showgrid=False, color=FONT_COLOR)
    return fig


# ─────────────────────────────────────────────────────────────
# DASHBOARD LAYOUT
# ─────────────────────────────────────────────────────────────

def delta_html(current, previous, higher_is_better=True):
    """Return a small colored delta string comparing current to previous session."""
    if previous is None:
        return ""
    diff = current - previous
    if abs(diff) < 0.05:
        return '<span style="color:#6b7280;font-size:0.8rem"> —</span>'
    arrow = "↑" if diff > 0 else "↓"
    good  = (diff > 0) == higher_is_better
    color = "#4ade80" if good else "#f87171"
    return f'<span style="color:{color};font-size:0.82rem"> {arrow}{abs(diff):.1f} vs yesterday</span>'


def render_dashboard(df, latest, profile, baselines, patterns, warnings, recommendations):
    """Render the full dashboard."""
    prev = df.iloc[-2] if len(df) >= 2 else None

    # ── Header ─────────────────────────────────────────────
    st.markdown(f"""
    <div class="dash-header">
        <h1>⚡ Recovery <span class="accent">Dashboard</span></h1>
        <p>Athlete performance tracking · {len(df)} session{"s" if len(df) != 1 else ""} logged
           · Last updated {latest["date"].strftime("%b %d, %Y") if pd.notna(latest["date"]) else "—"}
           · Sport: {latest.get("sport_type", "—")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Latest session KPI cards ────────────────────────────
    risk_class = str(latest.get("injury_risk", "—"))
    risk_color = {"HIGH": "#f87171", "MEDIUM": "#fbbf24", "LOW": "#4ade80"}.get(risk_class, "#e8eaf0")

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        d = delta_html(latest["recovery_score"], prev["recovery_score"] if prev is not None else None)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Recovery Score</div>
            <div class="metric-value">{int(latest["recovery_score"])}<span style="font-size:1.1rem;color:#6b7280">/100</span></div>
            <div class="metric-sub">Day {int(latest["day_number"])}{d}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Injury Risk</div>
            <div class="risk-value risk-{risk_class}" style="color:{risk_color}">{risk_class}</div>
            <div class="metric-sub">Classification</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        d = delta_html(latest["sleep_hours"], prev["sleep_hours"] if prev is not None else None)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Sleep</div>
            <div class="metric-value">{latest["sleep_hours"]}<span style="font-size:1.1rem;color:#6b7280">h</span></div>
            <div class="metric-sub">Last session{d}</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        d = delta_html(latest["hydration_liters"], prev["hydration_liters"] if prev is not None else None)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Hydration</div>
            <div class="metric-value">{latest["hydration_liters"]}<span style="font-size:1.1rem;color:#6b7280">L</span></div>
            <div class="metric-sub">Last session{d}</div>
        </div>""", unsafe_allow_html=True)

    with c5:
        d = delta_html(latest["protein_grams"], prev["protein_grams"] if prev is not None else None)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Protein</div>
            <div class="metric-value">{int(latest["protein_grams"])}<span style="font-size:1.1rem;color:#6b7280">g</span></div>
            <div class="metric-sub">Last session{d}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Baseline row ───────────────────────────────────────
    st.markdown('<div class="section-title">📊 Your Baseline</div>', unsafe_allow_html=True)

    b1, b2, b3, b4, b5 = st.columns(5)
    rs     = baselines["recovery_score"]
    sl     = baselines["sleep_hours"]
    hy     = baselines["hydration_liters"]
    pr     = baselines["protein_grams"]
    streak = baselines["low_risk_streak"]

    with b1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Recovery (7-Day)</div>
            <div class="metric-value" style="font-size:2rem">{rs["last7_mean"]}</div>
            <div class="metric-sub">All-time avg: {rs["all_mean"]} · Best: {rs["all_max"]}</div>
        </div>""", unsafe_allow_html=True)

    with b2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Sleep (7-Day)</div>
            <div class="metric-value" style="font-size:2rem">{sl["last7_mean"]}<span style="font-size:1rem;color:#6b7280">h</span></div>
            <div class="metric-sub">All-time avg: {sl["all_mean"]}h · Best: {sl["all_max"]}h</div>
        </div>""", unsafe_allow_html=True)

    with b3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Hydration (7-Day)</div>
            <div class="metric-value" style="font-size:2rem">{hy["last7_mean"]}<span style="font-size:1rem;color:#6b7280">L</span></div>
            <div class="metric-sub">All-time avg: {hy["all_mean"]}L</div>
        </div>""", unsafe_allow_html=True)

    with b4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Protein (7-Day)</div>
            <div class="metric-value" style="font-size:2rem">{int(pr["last7_mean"])}<span style="font-size:1rem;color:#6b7280">g</span></div>
            <div class="metric-sub">All-time avg: {int(pr["all_mean"])}g · Best: {int(pr["all_max"])}g</div>
        </div>""", unsafe_allow_html=True)

    with b5:
        streak_color = "#4ade80" if streak >= 3 else "#fbbf24" if streak >= 1 else "#f87171"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">LOW Risk Streak</div>
            <div class="metric-value" style="font-size:2rem;color:{streak_color}">{streak}</div>
            <div class="metric-sub">Consecutive sessions</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Pattern alerts ─────────────────────────────────────
    if patterns:
        st.markdown('<div class="section-title">🔍 Patterns Detected</div>', unsafe_allow_html=True)
        for p in patterns:
            is_positive = "trending upward" in p or "keep it up" in p.lower()
            pill = "pill-rec" if is_positive else "pill-warn"
            st.markdown(f'<div class="{pill}">{p}</div>', unsafe_allow_html=True)
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # ── Warnings & Recommendations ─────────────────────────
    col_warn, col_rec = st.columns(2)

    with col_warn:
        st.markdown('<div class="section-title">⚠ Warnings</div>', unsafe_allow_html=True)
        if warnings:
            for w in warnings:
                st.markdown(f'<div class="pill-warn">⚠ {w}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="pill-ok">✓ No major warnings today.</div>', unsafe_allow_html=True)

    with col_rec:
        st.markdown('<div class="section-title">✦ Recommendations</div>', unsafe_allow_html=True)
        for r in recommendations:
            st.markdown(f'<div class="pill-rec">→ {r}</div>', unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────────────
    st.markdown('<div class="section-title">📈 Trends</div>', unsafe_allow_html=True)

    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(chart_recovery_over_time(df), width="stretch")
    with g2:
        st.plotly_chart(chart_sleep_over_time(df), width="stretch")

    g3, g4 = st.columns(2)
    with g3:
        st.plotly_chart(chart_soreness_vs_intensity(df), width="stretch")
    with g4:
        st.plotly_chart(chart_hydration_protein(df), width="stretch")

    # ── Session history table ──────────────────────────────
    st.markdown('<div class="section-title">📋 Session History</div>', unsafe_allow_html=True)

    display_cols = [
        "day_number", "date", "sport_type",
        "sleep_hours", "hydration_liters", "protein_grams",
        "soreness_level", "training_intensity",
        "avg_heart_rate", "max_heart_rate",
        "recovery_score", "injury_risk"
    ]
    display_cols = [c for c in display_cols if c in df.columns]

    table_df = df[display_cols].copy()
    if "date" in table_df.columns:
        table_df["date"] = table_df["date"].dt.strftime("%b %d, %Y")

    table_df.columns = [c.replace("_", " ").title() for c in table_df.columns]

    def risk_style(val):
        colors = {"HIGH": "color: #f87171", "MEDIUM": "color: #fbbf24", "LOW": "color: #4ade80"}
        return colors.get(str(val), "")

    styled = (
        table_df.style
        .map(risk_style, subset=["Injury Risk"])
        .format({
            "Recovery Score":  "{:.0f}",
            "Sleep Hours":     "{:.1f}",
            "Hydration Liters":"{:.1f}",
            "Protein Grams":   "{:.0f}",
            "Avg Heart Rate":  "{:.0f}",
            "Max Heart Rate":  "{:.0f}",
        }, na_rep="—")
    )

    st.dataframe(styled, width="stretch", hide_index=True)


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────

df = load_data()

if df is None:
    st.markdown("""
    <div class="no-data">
        <h2>No sessions logged yet</h2>
        <p>Run <code>python injury_risk_recovery.py</code> to record your first session,<br>
           then refresh this page.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    latest          = df.iloc[-1]
    profile         = load_sport_profile_for_dashboard(latest.get("sport_type", "general"))
    baselines, df   = compute_baselines(df)
    patterns        = detect_patterns(df, profile)
    warnings        = derive_warnings(latest, profile)
    recommendations = derive_recommendations(latest, profile)
    render_dashboard(df, latest, profile, baselines, patterns, warnings, recommendations)
