
def forward_chaining(facts, rules):
    """
    Rule-based forward chaining inference engine.
    Starts with known facts and derives new facts.
    """

    known_facts = set(facts)
    explanation = []
    changed = True

    while changed:
        changed = False

        for rule in rules:
            conditions = set(rule["if"])
            conclusion = rule["then"]

            if conditions.issubset(known_facts):
                if conclusion not in known_facts:
                    known_facts.add(conclusion)
                    changed = True

                    explanation.append({
                        "rule": rule["name"],
                        "derived_fact": conclusion,
                        "reason": rule["description"]
                    })

    return {
        "facts": known_facts,
        "explanation": explanation
    }
