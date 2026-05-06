# Ishant Shah
# CS32 Final Project: Injury Risk & Recovery Analysis System

print("Welcome to the Injury Risk & Recovery Analysis System.")
print("This tool estimates recovery quality and injury risk based on daily habits.")
print()

import csv #for reading/writing csv files
import os #for checking if files exist on disk
import datetime #for recording today's date automatically
import requests #for making HTTP calls to external APIs
import matplotlib.pyplot as plt #for generating chart images


# ─────────────────────────────────────────────
# SPORT PROFILE LOADER
# Reads sport-specific thresholds from sport_profiles.csv.
# A coach can edit that file without touching this code.
# ─────────────────────────────────────────────
#AID from GAI
PROFILES_FILE = "sport_profiles.csv" #the function opens sport_profiles.csv, reads each row as a dictionary (column headers become keys), and searches for a matching sport. This is structured file reading — different from just printing to the screen.

DEFAULT_PROFILE = { #this is a dictionary that groups related values under named keys. The original code used standalone variables. Dictionaries let me pass all thresholds as a single object.
    "sport": "general", #^also removes hardcode
    "sleep_target": 8.0,
    "hydration_target": 3.0,
    "protein_target": 120.0,
    "max_safe_intensity": 8,
    "max_safe_hr": 185.0,
}


def load_sport_profile(sport_type):
    """
    Look up sport-specific thresholds from sport_profiles.csv.
    Falls back to the 'general' row if the sport isn't listed.
    """
    if not os.path.exists(PROFILES_FILE):
        print(f"[Profile] {PROFILES_FILE} not found. Using built-in defaults.")
        return DEFAULT_PROFILE.copy()

    sport_lower = sport_type.strip().lower()
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
        print(f"[Profile] '{sport_type}' not in profiles. Using general defaults.")
        return {
            "sport": "general",
            "sleep_target": float(general_row["sleep_target"]),
            "hydration_target": float(general_row["hydration_target"]),
            "protein_target": float(general_row["protein_target"]),
            "max_safe_intensity": int(general_row["max_safe_intensity"]),
            "max_safe_hr": float(general_row["max_safe_hr"]),
        }

    print(f"[Profile] No matching profile found. Using built-in defaults.")
    return DEFAULT_PROFILE.copy()


# ─────────────────────────────────────────────
# INPUT HELPERS
# ─────────────────────────────────────────────

def get_non_negative_float(prompt):
    """Ask the user for a non-negative float."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


def get_int_in_range(prompt, minimum, maximum):
    """Ask the user for an integer within a given range."""
    while True:
        try:
            value = int(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Please enter a number from {minimum} to {maximum}.")
        except ValueError:
            print("Please enter a valid integer.")


def get_choice(prompt, choices):
    """Ask the user for one of the allowed choices."""
    while True:
        value = input(prompt).strip().lower()
        if value in choices:
            return value
        print(f"Please enter one of these choices: {', '.join(choices)}")


# ─────────────────────────────────────────────
# SCORING FUNCTIONS
# Each function now accepts a sport-specific target
# read from sport_profiles.csv instead of being hardcoded.
# ─────────────────────────────────────────────

def calculate_sleep_score(sleep_hours, sleep_target=8.0): #before this it was hardcoded. Now it is not.
    """Return a score out of 25 based on sleep relative to the sport target."""
    if sleep_hours >= sleep_target: #all of these use sport specific targets
        return 25
    elif sleep_hours >= sleep_target - 1: #Instead of comparing against the hardcoded number 8, the function now accepts a sleep_target parameter.
        return 20
    elif sleep_hours >= sleep_target - 2: #The thresholds are computed relative to that target (target, target-1, target-2). This means the same function works correctly for any sport — a swimmer with a 9h target and a runner with a 7h target both get scored fairly. The =8.0 is a default parameter, so the function still works even if called the old way.
        return 15
    else:
        return 5


def calculate_hydration_score(hydration_liters, hydration_target=3.0): #same pattern — added hydration_target parameter, Uses percentages (67%, 50%) instead of hardcoded liters
    """Return a score out of 20 based on hydration relative to the sport target."""
    if hydration_liters >= hydration_target:
        return 20
    elif hydration_liters >= hydration_target * 0.67: #concept used here is proportional thresholds.
        return 15
    elif hydration_liters >= hydration_target * 0.5: #hydration_target * 0.67 means "67% of the target." This is more flexible than hardcoded numbers — if a marathon runner's target is 4L, then 67% of that is 2.68L, not the same 2L as before.
        return 10
    else:
        return 5


def calculate_protein_score(protein_grams, protein_target=120.0, supplement_use="no"):
    """
    Return a score out of 20 based on protein relative to the sport target.
    Supplement use gives a 10% boost to effective protein (partially compensates
    for lower dietary intake).
    """
    effective_protein = protein_grams * 1.1 if supplement_use == "yes" else protein_grams #The effective_protein line uses a conditional expression (also called a ternary operator): X if condition else Y. If the athlete uses supplements, their protein is boosted by 10% before scoring. This is a simple model of how supplements partially compensate for lower dietary intake. The actual scoring logic (the if/elif chain) is unchanged — only the input to that logic is adjusted
    if effective_protein >= protein_target:
        return 20
    elif effective_protein >= protein_target * 0.75:
        return 15
    elif effective_protein >= protein_target * 0.5:
        return 10
    else:
        return 5


def calculate_soreness_score(soreness_level):
    """
    Return a score out of 20 based on soreness.
    Lower soreness is generally better for recovery.
    """
    if soreness_level <= 2:
        return 20
    elif soreness_level <= 4:
        return 15
    elif soreness_level <= 6:
        return 10
    else:
        return 5


def calculate_intensity_score(training_intensity):
    """
    Return a score out of 15 based on training intensity.
    Lower daily intensity gives better immediate recovery.
    """
    if training_intensity <= 3:
        return 15
    elif training_intensity <= 6:
        return 10
    elif training_intensity <= 8:
        return 7
    else:
        return 3


def calculate_recovery_score(sleep_hours, hydration_liters, protein_grams,
                             soreness_level, training_intensity,
                             profile=None, supplement_use="no"):
    """Combine all subscores into one recovery score out of 100."""
    if profile is None:
        profile = DEFAULT_PROFILE

    sleep_score     = calculate_sleep_score(sleep_hours, profile["sleep_target"])
    hydration_score = calculate_hydration_score(hydration_liters, profile["hydration_target"])
    protein_score   = calculate_protein_score(protein_grams, profile["protein_target"], supplement_use)
    soreness_score  = calculate_soreness_score(soreness_level)
    intensity_score = calculate_intensity_score(training_intensity)

    return sleep_score + hydration_score + protein_score + soreness_score + intensity_score


def classify_injury_risk(recovery_score, soreness_level, training_intensity,
                         max_heart_rate=0, max_safe_hr=185):
    """
    Classify injury risk using recovery score, dangerous input combinations,
    and whether max heart rate exceeded the sport-specific safe limit.
    """
    hr_danger = max_heart_rate > max_safe_hr * 1.05

    if recovery_score < 45 or (soreness_level >= 8 and training_intensity >= 8) or hr_danger: #concept here is boolean flag derived from a calculation. hr_danger is a True/False value computed from a comparison. It's then used in the if statement with or. This means the function now has three independent paths to a HIGH classification: low score, dangerous soreness+intensity combo, or heart rate exceeding 105% of the sport's safe maximum
        return "HIGH"
    elif recovery_score < 70 or (soreness_level >= 6 and training_intensity >= 7):
        return "MEDIUM"
    else:
        return "LOW"


def generate_warnings(sleep_hours, hydration_liters, protein_grams,
                      soreness_level, training_intensity,
                      avg_heart_rate=0, max_heart_rate=0,
                      supplement_use="no", profile=None):
    """Create a list of warning messages based on input patterns."""
    if profile is None:
        profile = DEFAULT_PROFILE

    warnings = []

    if sleep_hours < profile["sleep_target"] - 2:
        warnings.append("Low sleep may reduce recovery and increase injury risk.")

    if hydration_liters < profile["hydration_target"] * 0.67:
        warnings.append("Low hydration may negatively affect performance and recovery.")

    if protein_grams < profile["protein_target"] * 0.5 and supplement_use == "no":
        warnings.append("Low protein intake may limit muscle recovery.")

    if soreness_level >= 7:
        warnings.append("High soreness may be a sign that your body needs more recovery.")

    if training_intensity >= profile["max_safe_intensity"]:
        warnings.append("Very high training intensity can increase strain on the body.")

    if max_heart_rate > profile["max_safe_hr"]:
        warnings.append(
            f"Max heart rate of {int(max_heart_rate)} bpm exceeded your sport's safe limit " #the int() inside the curly braces converts the float to a whole number right inside the string. Your original code used f-strings but only with plain variables
            f"of {int(profile['max_safe_hr'])} bpm — signs of overexertion."
        )

    if avg_heart_rate > profile["max_safe_hr"] * 0.85:
        warnings.append(
            f"Average heart rate of {int(avg_heart_rate)} bpm suggests sustained "
            f"high-intensity effort — monitor fatigue closely."
        )

    if sleep_hours < profile["sleep_target"] - 2 and training_intensity >= profile["max_safe_intensity"]: #reads a value from the profile dictionary and does math on it in the same expression.
        warnings.append("High intensity combined with low sleep is a risky recovery pattern.")

    if soreness_level >= 7 and training_intensity >= 7:
        warnings.append("High soreness plus hard training may increase injury risk.")

    return warnings


def generate_recommendations(sleep_hours, hydration_liters, protein_grams,
                             soreness_level, training_intensity,
                             supplement_use="no", profile=None):
    """
    Create actionable suggestions with specific numbers and sport-aware targets.
    Each recommendation tells the athlete exactly how much more they need.
    """
    if profile is None:
        profile = DEFAULT_PROFILE

    recommendations = []
    sport = profile["sport"]

    if sleep_hours < profile["sleep_target"]:
        extra = round(profile["sleep_target"] - sleep_hours, 1)
        recommendations.append(
            f"Try sleeping {extra} more hours to reach the {sport} target of {profile['sleep_target']}h." #concept here is computed recommendations. Your original code said generic things like "Try increasing sleep to at least 7 to 8 hours." The new version calculates the exact gap (extra = target - actual) and tells the athlete precisely how much more they need. The round(..., 1) ensures it shows one decimal place (e.g. "1.5 more hours" not "1.4999999")
        )

    if hydration_liters < profile["hydration_target"]:
        extra = round(profile["hydration_target"] - hydration_liters, 1)
        recommendations.append(
            f"Drink {extra} more liters of water to reach your {sport} target of {profile['hydration_target']}L."
        )

    effective_protein = protein_grams * 1.1 if supplement_use == "yes" else protein_grams
    if effective_protein < profile["protein_target"]:
        extra = round(profile["protein_target"] - protein_grams)
        supplement_note = " (supplements help, but whole food sources are more effective)" if supplement_use == "yes" else ""
        recommendations.append(
            f"Eat {extra} more grams of protein to reach your {sport} target "
            f"of {int(profile['protein_target'])}g{supplement_note}."
        )

    if soreness_level >= 7:
        recommendations.append(
            "Consider lighter training, mobility work, or an extra recovery day."
        )

    if training_intensity >= profile["max_safe_intensity"]:
        recommendations.append(
            f"Monitor hard training days carefully — {sport} athletes should avoid "
            f"stacking too many intensity {profile['max_safe_intensity']}+ sessions in a row."
        )

    if not recommendations:
        recommendations.append("Your habits look balanced today. Keep maintaining recovery.")

    return recommendations


# ═════════════════════════════════════════════
# FEATURE 1: API INTEGRATION
# Tries to fetch a sleep suggestion from a public API.
# Falls back to manual input if the API fails.
# ═════════════════════════════════════════════

def fetch_sleep_from_api():
    """
    Attempt to fetch a suggested sleep hours value from a public API.
    Uses Open Meteo (free, no key required) as a stand-in for a real
    wearable/health API. Returns a float or None if the request fails.
    """
    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=37.77&longitude=-122.41"
            "&hourly=temperature_2m&forecast_days=1"
        )
        response = requests.get(url, timeout=5) #sends an HTTP GET request to a remote server. timeout=5 means "give up after 5 seconds if the server doesn't respond." This is network programming — the program reaches out over the internet.
        response.raise_for_status() #checks if the server returned an error (like 404 or 500). If it did, this line raises an exception, which jumps to the except block. This is HTTP error handling.

        data = response.json() #the API returns data in JSON format (JavaScript Object Notation). .json() parses that text into a Python dictionary. JSON is the universal format for web APIs — understanding it is essential for any project that talks to the internet.
        temp = data["hourly"]["temperature_2m"][0] #this is nested data access. The JSON has a key "hourly" which contains a key "temperature_2m" which contains a list; [0] gets the first element. This is navigating a multi-level data structure.
        suggested_sleep = round(7.0 + (temp / 100), 1)
        suggested_sleep = max(5.0, min(suggested_sleep, 9.0))

        print(f"[API] Suggested sleep hours based on external data: {suggested_sleep}")
        return suggested_sleep

    except Exception as e: #catches any error (no internet, bad JSON, timeout, etc.) and stores the error message in e. The program prints the error but doesn't crash. This is graceful degradation — the system works with or without the API.
        print(f"[API] Could not fetch data ({e}). Falling back to manual input.")
        return None


def get_sleep_hours(): #as a wrapper — this function tries the API first, offers the user a choice, and falls back to manual input. This pattern of "try the automatic way, fall back to the manual way" is common in real software.
    """
    Try to get sleep hours from the API first.
    If the API fails or the user wants to override, fall back to manual input.
    """
    api_value = fetch_sleep_from_api()

    if api_value is not None:
        use_api = get_choice(
            f"Use suggested value of {api_value} hours? (yes / no): ",
            ["yes", "no"]
        )
        if use_api == "yes":
            return api_value

    return get_non_negative_float("Hours of sleep: ")


# ═════════════════════════════════════════════
# FEATURE 2: DATA PERSISTENCE (CSV)
# Saves every run's inputs and results to a CSV.
# Appends a new row each time the program runs.
# ═════════════════════════════════════════════

CSV_FILE = "recovery_log.csv"

CSV_HEADERS = [
    "date", "day_number",
    "sleep_hours", "hydration_liters", "protein_grams",
    "soreness_level", "training_intensity",
    "diet_type", "sport_type", "supplement_use",
    "avg_heart_rate", "max_heart_rate",
    "recovery_score", "injury_risk"
]


def get_day_number():
    """
    Count how many rows are already in the CSV to determine today's day number.
    Day 1 = first time the program is ever run.
    """
    if not os.path.exists(CSV_FILE): #checks if a file exists on disk before trying to read it. Without this, the program would crash on the first run when there's no CSV yet.
        return 1

    with open(CSV_FILE, "r", newline="") as f: #the "a" means append mode. Each run adds a row instead of overwriting the file. This is what makes the history build up over time. The newline="" prevents extra blank lines on Windows.
        reader = csv.reader(f)
        rows = list(reader)
        data_rows = len(rows) - 1 if len(rows) > 0 else 0
        return data_rows + 1


def save_to_csv(data_dict):
    """
    Append one row of data to the CSV log file.
    Creates the file with headers if it doesn't exist yet.
    """
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS) #writes a dictionary to CSV by matching dictionary keys to column headers. This is more robust than writing raw strings because the order of columns is handled automatically by the fieldnames list.

        if not file_exists:
            writer.writeheader() #writes the column names as the first row, but only on the very first run (if not file_exists). This conditional ensures the headers aren't duplicated every time.

        writer.writerow(data_dict)

    print(f"\n[CSV] Data saved to '{CSV_FILE}' (Day {data_dict['day_number']}).")


# ═════════════════════════════════════════════
# FEATURE 3: GRAPHING
# Reads the CSV and plots two charts:
#   1. Recovery score over time (by day)
#   2. Sleep hours vs. recovery score (scatter)
# Saves as PNG files since headless servers have no display.
# ═════════════════════════════════════════════

def load_csv_data():
    """
    Read all rows from the CSV log and return a list of dictionaries.
    Returns an empty list if the file doesn't exist or has no data rows.
    """
    if not os.path.exists(CSV_FILE):
        return []

    rows = []
    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def plot_recovery_over_time(rows):
    """
    Line chart: recovery score (y-axis) over day number (x-axis).
    Shows how your recovery trend changes across sessions.
    """
    day_numbers     = [int(row["day_number"]) for row in rows] #this is a compact way to build a list by transforming each item. It's equivalent to a for loop with .append(), but written in one line. It reads as: "for each row in rows, take the day_number and convert it to an int, and collect all of those into a list.
    recovery_scores = [int(row["recovery_score"]) for row in rows]

    plt.figure(figsize=(8, 4)) #creates a new chart canvas. figsize sets the width and height in inches.
    plt.plot(day_numbers, recovery_scores, marker="o", #draws a line chart. marker="o" adds dots at each data point. linewidth=2 makes the line thicker. label="..." is the text that appears in the legend
             color="steelblue", linewidth=2, label="Recovery Score")

    plt.axhline(y=70, color="orange", linestyle="--", label="Medium Risk Threshold (70)") #draws a horizontal reference line. This is a visual aid so the athlete can instantly see whether their score is above or below the risk thresholds
    plt.axhline(y=45, color="red",    linestyle="--", label="High Risk Threshold (45)")

    plt.title("Recovery Score Over Time")
    plt.xlabel("Day Number")
    plt.ylabel("Recovery Score (out of 100)")
    plt.ylim(0, 105)
    plt.legend()
    plt.tight_layout()
    plt.savefig("recovery_chart.png", bbox_inches="tight") #saves the chart as an image file instead of trying to display it on screen. This is necessary in headless environments like GitHub Codespaces
    plt.close() #releases the chart from memory after saving. Without this, matplotlib accumulates charts in memory
    print("[Graph] Saved as recovery_chart.png")


def plot_sleep_vs_recovery(rows):
    """
    Scatter plot: sleep hours (x-axis) vs. recovery score (y-axis).
    Helps visualize how sleep correlates with overall recovery.
    """
    sleep_values    = [float(row["sleep_hours"]) for row in rows]
    recovery_scores = [int(row["recovery_score"]) for row in rows]

    plt.figure(figsize=(8, 4))
    plt.scatter(sleep_values, recovery_scores,
                color="mediumseagreen", s=80, edgecolors="black", alpha=0.7)

    plt.title("Sleep Hours vs. Recovery Score")
    plt.xlabel("Sleep Hours")
    plt.ylabel("Recovery Score (out of 100)")
    plt.ylim(0, 105)
    plt.tight_layout()
    plt.savefig("sleep_chart.png", bbox_inches="tight")
    plt.close()
    print("[Graph] Saved as sleep_chart.png")


def show_graphs():
    """Load saved data and plot both charts."""
    rows = load_csv_data()

    if len(rows) == 0:
        print("\n[Graph] No saved data found. Run the program at least once to generate data.")
        return

    print(f"\n[Graph] Loaded {len(rows)} session(s) from '{CSV_FILE}'.")
    plot_recovery_over_time(rows)
    plot_sleep_vs_recovery(rows)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def main():
    """Run the injury risk and recovery analysis program."""
    print("Please enter your daily information below.")
    print()

    sleep_hours        = get_sleep_hours()
    hydration_liters   = get_non_negative_float("Hydration level (liters): ")
    protein_grams      = get_non_negative_float("Protein intake (grams): ")
    soreness_level     = get_int_in_range("Muscle soreness level (1-10): ", 1, 10)
    training_intensity = get_int_in_range("Training intensity (1-10): ", 1, 10)

    diet_type = get_choice(
        "Diet type (vegetarian / non-vegetarian / vegan): ",
        ["vegetarian", "non-vegetarian", "vegan"]
    )

    sport_type = input("Type of sport: ").strip()

    supplement_use = get_choice(
        "Do you use supplements? (yes / no): ",
        ["yes", "no"]
    )

    average_heart_rate = get_non_negative_float("Average heart rate during training: ")
    max_heart_rate     = get_non_negative_float("Max heart rate during training: ")

    # Load sport-specific thresholds from sport_profiles.csv
    profile = load_sport_profile(sport_type)
    print(f"[Profile] Using thresholds for: {profile['sport']}")
    print()

    recovery_score = calculate_recovery_score(
        sleep_hours, hydration_liters, protein_grams,
        soreness_level, training_intensity,
        profile=profile, supplement_use=supplement_use
    )

    injury_risk = classify_injury_risk(
        recovery_score, soreness_level, training_intensity,
        max_heart_rate=max_heart_rate, max_safe_hr=profile["max_safe_hr"]
    )

    warnings = generate_warnings(
        sleep_hours, hydration_liters, protein_grams,
        soreness_level, training_intensity,
        avg_heart_rate=average_heart_rate, max_heart_rate=max_heart_rate,
        supplement_use=supplement_use, profile=profile
    )

    recommendations = generate_recommendations(
        sleep_hours, hydration_liters, protein_grams,
        soreness_level, training_intensity,
        supplement_use=supplement_use, profile=profile
    )

    print("----- DAILY REPORT -----")
    print(f"Sport:                    {sport_type}")
    print(f"Diet type:                {diet_type}")
    print(f"Supplements used:         {supplement_use}")
    print(f"Average heart rate:       {average_heart_rate} bpm")
    print(f"Max heart rate:           {max_heart_rate} bpm")
    print(f"Recovery score:           {recovery_score}/100")
    print(f"Injury risk:              {injury_risk}")
    print()

    print("Warnings:")
    if warnings:
        for warning in warnings:
            print(f"  - {warning}")
    else:
        print("  - No major warnings today.")

    print()
    print("Recommendations:")
    for rec in recommendations:
        print(f"  - {rec}")

    day_number   = get_day_number()
    session_data = {
        "date":               datetime.date.today().isoformat(),
        "day_number":         day_number,
        "sleep_hours":        sleep_hours,
        "hydration_liters":   hydration_liters,
        "protein_grams":      protein_grams,
        "soreness_level":     soreness_level,
        "training_intensity": training_intensity,
        "diet_type":          diet_type,
        "sport_type":         sport_type,
        "supplement_use":     supplement_use,
        "avg_heart_rate":     average_heart_rate,
        "max_heart_rate":     max_heart_rate,
        "recovery_score":     recovery_score,
        "injury_risk":        injury_risk,
    }
    save_to_csv(session_data)

    print()
    view_graphs = get_choice(
        "Would you like to see your recovery graphs? (yes / no): ",
        ["yes", "no"]
    )
    if view_graphs == "yes":
        show_graphs()


main()
