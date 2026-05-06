# --------------------------------------------------
# SCORING FUNCTIONS
# --------------------------------------------------

def calculate_sleep_score(sleep_hours):
    """
    Professional guideline note:
    7-9 hours is commonly recommended for recovery.
    """
    if sleep_hours >= 8:
        return 25
    elif sleep_hours >= 6:
        return 15
    else:
        return 5


def calculate_hydration_score(hydration_liters):
    """
    Professional guideline note:
    Around 2-3 liters per day is a simple baseline guideline,
    though athletes may need more depending on training.
    """
    if hydration_liters >= 3:
        return 20
    elif hydration_liters >= 2:
        return 15
    else:
        return 5


def calculate_soreness_score(soreness_level):
    """
    Professional guideline note:
    Low soreness is usually more compatible with good recovery.
    High soreness may suggest incomplete recovery.
    """
    if soreness_level <= 3:
        return 20
    elif soreness_level <= 6:
        return 10
    else:
        return 0


def calculate_nutrition_score(protein_met, supplements_used):
    """
    Simplified nutrition model:
    - Meeting protein goal helps recovery.
    - Supplements are optional and only add a small bonus in this model.
    """
    score = 0

    if protein_met == "yes":
        score += 15
    else:
        score += 5

    if supplements_used == "yes":
        score += 5

    return score


def calculate_training_score(training_intensity):
    """
    Professional guideline note:
    Moderate training is often a balanced zone.
    High intensity without recovery can elevate risk.
    """
    if training_intensity == "moderate":
        return 15
    elif training_intensity == "low":
        return 10
    else:  # high
        return 5


# --------------------------------------------------
# RECOVERY + RISK FUNCTIONS
# --------------------------------------------------

def calculate_recovery_score(
    sleep_score,
    hydration_score,
    soreness_score,
    nutrition_score,
    training_score
):
    """Return total recovery score out of 100."""
    return (
        sleep_score
        + hydration_score
        + soreness_score
        + nutrition_score
        + training_score
    )


def calculate_injury_risk(
    sleep_hours,
    hydration_liters,
    soreness_level,
    training_intensity,
    protein_met
):
    """
    Rule-based injury risk calculation.
    Higher score = greater risk.
    """
    risk_points = 0

    if sleep_hours < 6:
        risk_points += 20

    if hydration_liters < 2:
        risk_points += 15

    if soreness_level >= 7:
        risk_points += 20
    elif soreness_level >= 4:
        risk_points += 10

    if training_intensity == "high":
        risk_points += 15

    if protein_met == "no":
        risk_points += 10

    # Interaction rules: combinations matter
    if sleep_hours < 6 and training_intensity == "high":
        risk_points += 20

    if soreness_level >= 7 and training_intensity == "high":
        risk_points += 15

    if hydration_liters < 2 and training_intensity == "high":
        risk_points += 10

    return risk_points


def classify_injury_risk(risk_points):
    """Convert numeric risk points into a category."""
    if risk_points >= 50:
        return "HIGH"
    elif risk_points >= 25:
        return "MEDIUM"
    else:
        return "LOW"


# --------------------------------------------------
# WARNING + RECOMMENDATION FUNCTIONS
# --------------------------------------------------

def generate_warnings(
    sleep_hours,
    hydration_liters,
    soreness_level,
    training_intensity,
    protein_met
):
    """Generate warning messages based on user inputs."""
    warnings = []

    if sleep_hours < 6:
        warnings.append("Low sleep detected.")

    if hydration_liters < 2:
        warnings.append("Hydration is below the recommended range in this model.")

    if soreness_level >= 7:
        warnings.append("High soreness detected.")

    if protein_met == "no":
        warnings.append("Protein intake may be too low for optimal recovery.")

    if sleep_hours < 6 and training_intensity == "high":
        warnings.append("High training intensity combined with low sleep may elevate injury risk.")

    if soreness_level >= 7 and training_intensity == "high":
        warnings.append("High soreness combined with intense training suggests incomplete recovery.")

    return warnings


def generate_recommendations(
    sleep_hours,
    hydration_liters,
    soreness_level,
    training_intensity,
    protein_met,
    diet_type
):
    """Generate simple recommendations."""
    recommendations = []

    if sleep_hours < 7:
        recommendations.append("Aim for about 7-9 hours of sleep to support recovery.")

    if hydration_liters < 2:
        recommendations.append("Increase hydration toward at least 2-3 liters per day.")

    if soreness_level >= 7:
        recommendations.append("Consider rest, lighter training, stretching, or active recovery.")

    if protein_met == "no":
        if diet_type == "vegetarian":
            recommendations.append(
                "Increase protein intake using foods such as Greek yogurt, tofu, beans, lentils, or protein shakes."
            )
        else:
            recommendations.append(
                "Increase protein intake to better support muscle repair and recovery."
            )

    if training_intensity == "high" and (sleep_hours < 6 or soreness_level >= 7):
        recommendations.append(
            "Reduce training intensity temporarily until recovery improves."
        )

    if not recommendations:
        recommendations.append("Your current habits look fairly balanced in this model. Keep monitoring recovery daily.")

    return recommendations


# --------------------------------------------------
# OUTPUT FUNCTION
# --------------------------------------------------

def display_results(
    name,
    sport,
    diet_type,
    sleep_score,
    hydration_score,
    soreness_score,
    nutrition_score,
    training_score,
    recovery_score,
    risk_points,
    risk_level,
    warnings,
    recommendations
):
    """Display a clean final report."""
    print("\n" + "=" * 55)
    print("DAILY RECOVERY REPORT")
    print("=" * 55)
    print(f"Athlete: {name}")
    print(f"Sport: {sport}")
    print(f"Diet type: {diet_type}")

    print("\nCategory Scores:")
    print(f"- Sleep score: {sleep_score}/25")
    print(f"- Hydration score: {hydration_score}/20")
    print(f"- Soreness score: {soreness_score}/20")
    print(f"- Nutrition score: {nutrition_score}/20")
    print(f"- Training score: {training_score}/15")

    print(f"\nRecovery Score: {recovery_score}/100")
    print(f"Injury Risk Points: {risk_points}")
    print(f"Injury Risk Classification: {risk_level}")

    print("\nWarnings:")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- No major warnings detected today.")

    print("\nRecommendations:")
    for recommendation in recommendations:
        print(f"- {recommendation}")

    print("\nNote:")
    print("This tool is a simplified computational model and not a medical or diagnostic system.")
    print("=" * 55)
