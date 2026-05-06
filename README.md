# Injury Risk & Recovery Analysis System
**Ishant Shah — CS32 Final Project**

---

## Overview

This project is a rule-based system that analyzes an athlete's daily habits to estimate recovery quality and classify injury risk. The goal is to take a complex real-world problem — injury prevention — and model it computationally using simplified, observable inputs and logical scoring rules.

Rather than measuring biological factors directly, the system uses behavioral data such as sleep, hydration, protein intake, training intensity, and soreness to detect patterns associated with poor recovery or elevated injury risk.

The project includes a CLI tool for daily data entry and a Streamlit dashboard for visualizing trends across sessions.

> **Disclaimer:** This tool is not a medical or diagnostic instrument. It is a computational model designed to raise awareness of how daily habits relate to recovery and injury risk.

---

## Problem Statement

Athletes often struggle to recognize when their body is at risk of injury due to poor recovery, inconsistent nutrition, or excessive training load. This project addresses the question:

> *"Can we estimate injury risk using daily behavioral input and simple computational rules?"*

---

## Features

| Feature | Description |
|---|---|
| Daily input system | Collects sleep, hydration, protein, soreness, training intensity, heart rate, diet, and sport type |
| Recovery score | Combines subscores into a single 0–100 recovery score |
| Injury risk classification | Classifies risk as LOW, MEDIUM, or HIGH using rule-based logic |
| Warnings | Flags dangerous combinations (e.g. high intensity + low sleep) |
| Recommendations | Gives sport-aware advice with exact targets (e.g. "drink 1.2 more liters") |
| Sport profiles | Loads per-sport thresholds from `sport_profiles.csv` |
| API integration | Fetches a sleep suggestion from an external API with manual fallback |
| Data persistence | Appends every session to `recovery_log.csv` for historical tracking |
| Matplotlib graphs | Saves recovery and sleep trend charts as PNG files |
| Streamlit dashboard | Reads `recovery_log.csv` and renders live charts, baselines, and session history |

---

## Inputs

The program collects the following data each session:

- Hours of sleep
- Hydration level (liters)
- Protein intake (grams)
- Muscle soreness level (1–10)
- Training intensity (1–10)
- Average and max heart rate during training
- Type of sport
- Diet type (vegetarian / non-vegetarian / vegan)
- Supplement usage (yes / no)

---

## Outputs

- A **recovery score** out of 100
- An **injury risk classification** — LOW, MEDIUM, or HIGH
- **Warnings** about risky input patterns
- **Recommendations** with specific, sport-aware targets
- A **CSV log** (`recovery_log.csv`) of all sessions
- **PNG charts** of recovery and sleep trends
- A **Streamlit dashboard** (`app.py`) with interactive charts and session history

---

## Computational Approach

Each input is converted into a subscore using conditional logic. The subscores are summed into a total recovery score, which is then combined with specific high-risk patterns to classify injury risk.

| Subscore | Max Points | Key Logic |
|---|---|---|
| Sleep | 25 | Compared against sport-specific sleep target |
| Hydration | 20 | Compared against sport-specific hydration target |
| Protein | 20 | Adjusted for supplement use; compared against sport target |
| Soreness | 20 | Lower soreness = higher score |
| Training intensity | 15 | Lower intensity = higher score |
| **Total** | **100** | |

**Risk classification thresholds:**
- **LOW** — score ≥ 70, no dangerous input combinations
- **MEDIUM** — score 45–69, or soreness ≥ 6 with intensity ≥ 7
- **HIGH** — score < 45, soreness ≥ 8 with intensity ≥ 8, or max heart rate exceeding the sport's safe limit

---

## Key CS Concepts

**Abstraction** — complex biology (fatigue, overtraining, inflammation) is reduced to measurable daily inputs and numeric scores.

**Decomposition** — the problem is broken into independent scoring functions, each handling one input dimension, which are then combined.

**Algorithm design** — rule-based conditional logic computes scores, detects dangerous patterns, and generates targeted recommendations.

**Pattern recognition** — the dashboard detects multi-session trends such as consecutive high-soreness days, chronic low sleep, and improving or declining recovery trajectories.

---

## Project Structure

```
cs32-final-project/
├── injury_risk_recovery.py   # Main CLI program — collects input, scores, saves CSV
├── app.py                    # Streamlit dashboard — reads CSV and renders charts
├── sport_profiles.csv        # Per-sport thresholds (editable without touching code)
├── recovery_log.csv          # Auto-generated session log (created on first run)
├── recovery_chart.png        # Auto-generated recovery trend chart
└── sleep_chart.png           # Auto-generated sleep vs recovery chart
```

---

## How to Run

**Step 1 — Log a session (repeat to build up data):**
```bash
python injury_risk_recovery.py
```

**Step 2 — Launch the dashboard:**
```bash
streamlit run app.py
```

In GitHub Codespaces, open the **PORTS** tab and click the globe icon next to port **8501** to view the dashboard.

**Install dependencies (first time only):**
```bash
pip install requests matplotlib streamlit pandas plotly
```

---

## AI Acknowledgment

The core scoring logic, input validation, and rule-based classification in `injury_risk_recovery.py` were written independently as part of CS32 coursework.

The following extensions were built with assistance from Claude (Anthropic):

- **Sport profile system** — helped design the CSV-based configuration loader so thresholds vary by sport without hardcoding.
- **API integration** — helped structure the HTTP request, JSON parsing, and try/except fallback for when the API is unavailable.
- **CSV persistence and graphing** — helped implement append-mode file writing and the matplotlib chart functions.
- **Streamlit dashboard (`app.py`)** — helped build the dashboard including Plotly charts, Pandas data loading, rolling averages, pattern detection, and custom styling.

All code was reviewed, understood, and tested by the author before submission.

---

## Dashboard Sections

- **Latest session cards** — recovery score, injury risk, sleep, hydration, protein with delta vs. previous session
- **7-day baseline cards** — rolling averages and all-time bests
- **Pattern detection** — multi-session alerts (e.g. chronic low sleep, consecutive high-intensity days)
- **Warnings & recommendations** — derived from the latest session using sport-specific thresholds
- **Trend charts** — recovery over time, sleep per session, soreness vs. intensity, hydration & protein
- **Session history table** — full log with color-coded injury risk column
