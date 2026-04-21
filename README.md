# cs32-final-project
Ishant Shah's CS32 Final Project - individual
CS32 Final Project: Injury Risk & Recovery Analysis System

Project overview is as below:
This project is a rule-based system that analyzes an athlete’s daily habits to estimate recovery
quality and injury risk. The goal is to take a complex real-world problem—injury prevention—and
model it computationally using simplified inputs and logical rules. Instead of directly measuring
biological factors, this program uses observable behaviors such as sleep, training intensity, diet
and soreness to identify patterns that may indicate poor recovery or increased injury risk.

The problem statement is:
Atheletes often struggle to recognise when their body is at risk or injury due to poor recovery,
incosnsitent nutrition, or excesive training. This project aims to answer the question - "can we estimate injury risk using daily behavioural input and simple computation rules?"

Input of the program are as below:
The program collects daily user data, inclduing:
- hours of sleep
- diet (e.g., vegetarian, non-vegetarian, vegan) - plan to add more specifc ones like red meat only, pascetarian, gluten free etc
- type of sport
- training intensity (1–10 scale) and/or heart rate data
- Supplement usage (yes/no)
- protein intake
- hydration level
- muscle soreness level (1–10 scale)

The outputs are:
- a recovery score
- an injury risk classification (low, medium,high)
- warnings about potential recovery or nutrition issues
- recommendations for improvement based on rule-based logic - planning on making the reccomendations links, or advise from professional nutrionists, physiotherapists, athletes, etc

Computational approach is:
- each input contributes to a recovery or a risk score
- conditional logic is used to detect concerning patterns
- scores are combined to classify injury risk levels

Key concepts i plan to use:
- abstraction: simplifying key complex biology into measureable inputs
- decomposition: breaking the problem into smaller components
-algorithm desgin: using rule-based logic to compute scores and classifications
- pattern recognition: identifying trends that increase risk of injury

Features of the output:
- daily input system
- recovery score calculation
- injury risk calculation
- reccomendation generation

Scope of this project is not intended to be medical or a disgnostic tool, but just to use computational model to bring awareness to daily habits and its relationship to injuries.


