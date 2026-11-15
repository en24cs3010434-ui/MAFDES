
def backward_chaining(goal, facts, rules, visited=None):
    """
    Educational backward chaining inference engine.
    Checks whether a goal can be established
    from known facts and predefined rules.
    """

    if visited is None:
        visited = set()

    if goal in facts:
        return {
            "success": True,
            "goal": goal,
            "reason": "Goal is already present in known facts."
        }

    if goal in visited:
        return {
            "success": False,
            "goal": goal,
            "reason": "Circular dependency detected."
        }

    visited.add(goal)

    for rule in rules:
        if rule["then"] == goal:
            results = []

            for condition in rule["if"]:
                result = backward_chaining(
                    condition, facts, rules, visited.copy()
                )
                results.append(result)

            if all(item["success"] for item in results):
                return {
                    "success": True,
                    "goal": goal,
                    "reason": rule["description"],
                    "rule": rule["name"],
                    "conditions": results
                }

    return {
        "success": False,
        "goal": goal,
        "reason": "Required evidence or supporting rule not found."
    }
