
from engine.forward_chaining import forward_chaining
from engine.backward_chaining import backward_chaining
from engine.certainty_factor import certainty_percentage

from knowledge_base.rules import AIRCRAFT_RULES
from knowledge_base.facts import generate_facts


def diagnose_aircraft(inputs):

    # Step 1: Generate facts from user inputs
    facts = generate_facts(inputs)

    # Step 2: Apply forward chaining
    forward_result = forward_chaining(
        facts,
        AIRCRAFT_RULES
    )

    derived_facts = forward_result["facts"]

    # Step 3: Prepare diagnosis results
    diagnoses = []

    for rule in AIRCRAFT_RULES:

        conclusion = rule["then"]

        if conclusion in derived_facts:

            confidence = certainty_percentage(
                [rule["cf"]]
            )

            diagnoses.append({
                "rule": rule["name"],
                "diagnosis": conclusion.replace("_", " ").title(),
                "confidence": confidence,
                "explanation": rule["description"]
            })

    # Step 4: Backward chaining verification
    goals = [
        "power_status_uncertain",
        "cooling_status_uncertain",
        "sensor_data_inconsistent",
        "system_review_required",
        "simulation_status_normal"
    ]

    verification = {}

    for goal in goals:
        verification[goal] = backward_chaining(
            goal,
            facts,
            AIRCRAFT_RULES
        )

    # Step 5: Return complete results
    return {
        "input_facts": facts,
        "derived_facts": list(derived_facts),
        "diagnoses": diagnoses,
        "explanation": forward_result["explanation"],
        "verification": verification
    }
