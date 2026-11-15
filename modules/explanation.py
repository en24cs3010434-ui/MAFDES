
def generate_explanation(diagnosis_result):

    explanations = []

    for item in diagnosis_result.get("explanation", []):

        explanations.append({
            "rule_name": item["rule"],
            "derived_fact": item["derived_fact"].replace(
                "_", " "
            ).title(),
            "reason": item["reason"]
        })

    if not explanations:
        explanations.append({
            "rule_name": "NO_MATCH",
            "derived_fact": "No additional finding",
            "reason": "No predefined diagnostic rule was triggered."
        })

    return explanations


def generate_summary(diagnosis_result):

    diagnoses = diagnosis_result.get("diagnoses", [])

    if not diagnoses:
        return "No diagnostic finding was generated."

    summary = []

    for item in diagnoses:
        summary.append(
            f"{item['diagnosis']} - "
            f"Confidence estimate: {item['confidence']}%"
        )

    return "\n".join(summary)
