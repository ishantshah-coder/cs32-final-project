#Step3.py

# Project components:
# - Input system (collects daily data)
# - Scoring system (sleep, hydration, nutrition, etc.)
# - Recovery score calculator
# - Injury risk classifier
# - Warning system
# - Recommendation generator
# - Output display


# Algorithms
# Example Input:
# sleep: 5 hours
# hydration: 1.5L
# soreness: 7
# intensity: high
# protein: low

# Example Output
# recovery score: 45
# injury risk: HIGH
# warnings + recommendations

def calculate_sleep_score(sleep):
    if sleep >= 8:
        return 25
    elif sleep >= 6:
        return 15
    else:
        return 5

def calculate_hydration_score(hydration):
    if hydration >= 3:
        return 20
    elif hydration >= 2:
        return 15
    else:
        return 5

sleep = 5
hydration = 1.5

print(calculate_sleep_score(sleep))
print(calculate_hydration_score(hydration))




