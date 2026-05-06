# Injury Risk & Recovery Analysis System
**Ishant Shah — CS32 Final Project**

---

## Overview

This project is a rule-based system that analyzes an athlete's daily habits to estimate recovery quality and classify injury risk. The goal is to take a complex real-world problem — injury prevention — and model it computationally using simplified, observable inputs and logical scoring rules.

Rather than measuring biological factors directly, the system uses behavioral data such as sleep, hydration, protein intake, training intensity, and soreness level to detect patterns associated with poor recovery or elevated injury risk. The project is accompanied by a live Streamlit dashboard that visualizes trends across sessions.

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
| Warnings | Flags dangerous combinations of inputs, such as high intensity combined with low sleep |
| Recommendations | Gives specific, sport-aware advice with exact targets, such as drinking more water or increasing protein |
| Sport profiles | Can load per-sport thresholds from `sport_profiles.csv`; if the file is missing, the program uses built-in default values |
| API integration | Fetches a sleep suggestion from an external API with a manual override fallback |
| Data persistence | Appends every session to `recovery_log.csv` for historical tracking |
| Matplotlib graphs | Saves recovery-over-time and sleep-vs-recovery charts as PNG files |
| Streamlit dashboard | Reads `recovery_log.csv` and renders live charts, warnings, baselines, and session history |

---

## Inputs

The program collects the following data each session:

- Hours of sleep
- Hydration level in liters
- Protein intake in grams
- Muscle soreness level on a 1–10 scale
- Training intensity on a 1–10 scale
- Average and max heart rate during training
- Type of sport
- Diet type: vegetarian, non-vegetarian, or vegan
- Supplement usage: yes or no

**Possible future additions:** more detailed diet categories, more sport-specific profiles, and research-supported recommendation links.

---

## Outputs

- A **recovery score** out of 100
- An **injury risk classification** — LOW, MEDIUM, or HIGH
- **Warnings** about potentially risky input patterns
- **Recommendations** with specific targets tailored to the athlete's sport
- A **CSV log** called `recovery_log.csv` that stores all sessions
- **PNG charts** of recovery and sleep trends saved locally
- A **Streamlit dashboard** called `app.py` with interactive charts and session history

---

## Computational Approach

Each input is converted into a subscore using conditional logic. The subscores are summed into a total recovery score, which is then used alongside specific high-risk combinations to classify injury risk.

| Subscore | Max Points | Key Logic |
|---|---:|---|
| Sleep | 25 | Compared against sport-specific sleep target |
| Hydration | 20 | Compared against sport-specific hydration target |
| Protein | 20 | Adjusted for supplement use and compared against sport target |
| Soreness | 20 | Lower soreness gives a higher score |
| Training intensity | 15 | Lower daily intensity gives a higher immediate recovery score |
| **Total** | **100** | Combined recovery score |

**Risk classification thresholds:**

- **LOW** — score ≥ 70 and no dangerous input combinations
- **MEDIUM** — score 45–69, or soreness ≥ 6 with intensity ≥ 7
- **HIGH** — score < 45, soreness ≥ 8 with intensity ≥ 8, or max heart rate exceeding the sport's safe limit

---

## Key CS Concepts

**Abstraction** — complex biology, such as fatigue, overtraining, and recovery, is reduced to measurable daily inputs and simple numeric scores.

**Decomposition** — the problem is broken into smaller functions, such as input validation, scoring, warning generation, recommendation generation, CSV saving, and graphing.

**Algorithm design** — rule-based conditional logic is used to compute scores, detect dangerous patterns, and generate targeted recommendations.

**Pattern recognition** — the dashboard detects multi-session trends such as consecutive high-soreness days, chronic low sleep, repeated high-intensity days, and improving or declining recovery trajectories.

**Data persistence** — the program saves each session to a CSV file so that the athlete can build a personal recovery history over time.

**Data visualization** — the dashboard turns stored recovery data into graphs, baselines, and trend summaries.

**API integration** — the command-line program includes an external API request for a suggested sleep value, with a fallback to manual input if the API fails.

---

## Project Structure

```text
cs32-final-project/
├── injury_risk_recovery.py   # Main CLI program — collects input, scores, saves CSV
├── app.py                    # Streamlit dashboard — reads CSV and renders charts
├── sport_profiles.csv        # Optional: per-sport thresholds; program uses defaults if missing
├── recovery_log.csv          # Auto-generated session log, created on first run
├── recovery_chart.png        # Auto-generated recovery trend chart
└── sleep_chart.png           # Auto-generated sleep vs recovery chart
