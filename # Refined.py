# Refined
# Ishant Shah
# CS32 Final Project: Injury Risk & Recovery Analysis System

print("Welcome to the Injury Risk & Recovery Analysis System.")
print("This tool estimates recovery quality and injury risk based on daily habits.")
print()


def get_non_negative_float(prompt): #repeatedly prompts the user for input using a while True loop until they enter a valid non-negative number, ensuring the program only continues with correct data
    """Ask the user for a non-negative float."""
    while True:
        try:
            value = float(input(prompt)) #float() function converts a value (usually a string from user input) into a decimal number (a floating-point number) so it can be used in calculations.
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


def get_int_in_range(prompt, minimum, maximum): #repeatedly ask the user for input until they enter a valid integer within a specified range, ensuring the program only accepts appropriate values
    """Ask the user for an integer within a given range."""
    while True:
        try:
            value = int(input(prompt)) #int(input(...)) converts the input into an integer
            if minimum <= value <= maximum:
                return value
            print(f"Please enter a number from {minimum} to {maximum}.")
        except ValueError:
            print("Please enter a valid integer.")


def get_choice(prompt, choices): #repeatedly prompt the user until they enter a valid choice from a predefined list of options, ensuring only acceptable inputs are returned.
    """Ask the user for one of the allowed choices."""
    while True:
        value = input(prompt).strip().lower()
        if value in choices:
            return value
        print(f"Please enter one of these choices: {', '.join(choices)}") #if asked if vegan or meat eater, cant write anyting else etc. 


def calculate_sleep_score(sleep_hours):
    """Return a score out of 25 based on sleep."""
    if sleep_hours >= 8:
        return 25
    elif sleep_hours >= 7:
        return 20
    elif sleep_hours >= 6:
        return 15
    else:
        return 5


def calculate_hydration_score(hydration_liters):
    """Return a score out of 20 based on hydration."""
    if hydration_liters >= 3:
        return 20
    elif hydration_liters >= 2:
        return 15
    elif hydration_liters >= 1.5:
        return 10
    else:
        return 5


def calculate_protein_score(protein_grams):
    """Return a score out of 20 based on protein intake."""
    if protein_grams >= 120:
        return 20
    elif protein_grams >= 90:
        return 15
    elif protein_grams >= 60:
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
                             soreness_level, training_intensity):
    """Combine all subscores into one recovery score out of 100."""
    sleep_score = calculate_sleep_score(sleep_hours)
    hydration_score = calculate_hydration_score(hydration_liters)
    protein_score = calculate_protein_score(protein_grams)
    soreness_score = calculate_soreness_score(soreness_level)
    intensity_score = calculate_intensity_score(training_intensity)

    total_score = (
        sleep_score
        + hydration_score
        + protein_score
        + soreness_score
        + intensity_score
    )

    return total_score


def classify_injury_risk(recovery_score, soreness_level, training_intensity):
    """
    Classify injury risk using both the recovery score and
    some especially concerning combinations.
    """
    if recovery_score < 45 or (soreness_level >= 8 and training_intensity >= 8):
        return "HIGH"
    elif recovery_score < 70 or (soreness_level >= 6 and training_intensity >= 7):
        return "MEDIUM"
    else:
        return "LOW"


def generate_warnings(sleep_hours, hydration_liters, protein_grams,
                      soreness_level, training_intensity):
    """Create a list of warning messages based on input patterns."""
    warnings = []

    if sleep_hours < 6:
        warnings.append("Low sleep may reduce recovery and increase injury risk.")

    if hydration_liters < 2:
        warnings.append("Low hydration may negatively affect performance and recovery.")

    if protein_grams < 60:
        warnings.append("Low protein intake may limit muscle recovery.")

    if soreness_level >= 7:
        warnings.append("High soreness may be a sign that your body needs more recovery.")

    if training_intensity >= 8:
        warnings.append("Very high training intensity can increase strain on the body.")

    if sleep_hours < 6 and training_intensity >= 8:
        warnings.append("High intensity combined with low sleep is a risky recovery pattern.")

    if soreness_level >= 7 and training_intensity >= 7:
        warnings.append("High soreness plus hard training may increase injury risk.")

    return warnings


def generate_recommendations(sleep_hours, hydration_liters, protein_grams,
                             soreness_level, training_intensity):
    """Create a list of suggestions for improvement."""
    recommendations = []

    if sleep_hours < 7:
        recommendations.append("Try increasing sleep to at least 7 to 8 hours.")

    if hydration_liters < 2:
        recommendations.append("Increase daily water intake and hydrate more during training.")

    if protein_grams < 90:
        recommendations.append("Increase protein intake through meals or supplements if needed.")

    if soreness_level >= 7:
        recommendations.append("Consider lighter training, mobility work, or an extra recovery day.")

    if training_intensity >= 8:
        recommendations.append("Monitor hard training days carefully and avoid stacking too many in a row.")

    if not recommendations:
        recommendations.append("Your habits look balanced today. Keep maintaining recovery.")

    return recommendations


def main():
    """Run the injury risk and recovery analysis program."""
    print("Please enter your daily information below.")
    print()

    sleep_hours = get_non_negative_float("Hours of sleep: ")
    hydration_liters = get_non_negative_float("Hydration level (liters): ")
    protein_grams = get_non_negative_float("Protein intake (grams): ")
    soreness_level = get_int_in_range("Muscle soreness level (1-10): ", 1, 10)
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
    max_heart_rate = get_non_negative_float("Max heart rate during training: ")

    recovery_score = calculate_recovery_score(
        sleep_hours,
        hydration_liters,
        protein_grams,
        soreness_level,
        training_intensity
    )

    injury_risk = classify_injury_risk(
        recovery_score,
        soreness_level,
        training_intensity
    )

    warnings = generate_warnings(
        sleep_hours,
        hydration_liters,
        protein_grams,
        soreness_level,
        training_intensity
    )

    recommendations = generate_recommendations(
        sleep_hours,
        hydration_liters,
        protein_grams,
        soreness_level,
        training_intensity
    )

    print()
    print("----- DAILY REPORT -----")
    print(f"Sport: {sport_type}")
    print(f"Diet type: {diet_type}")
    print(f"Supplements used: {supplement_use}")
    print(f"Average heart rate: {average_heart_rate}")
    print(f"Max heart rate: {max_heart_rate}")
    print(f"Recovery score: {recovery_score}/100")
    print(f"Injury risk classification: {injury_risk}")
    print()

    print("Warnings:")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No major warnings today.")

    print()
    print("Recommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")


main()
