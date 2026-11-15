
def calculate_certainty(factors):
    """
    Calculate combined certainty factor
    for an educational rule-based expert system.

    Each factor must be between -1 and 1.
    """

    if not factors:
        return 0.0

    if any(not -1 <= cf <= 1 for cf in factors):
        raise ValueError("Each certainty factor must be between -1 and 1.")

    combined = factors[0]

    for cf in factors[1:]:
        if combined >= 0 and cf >= 0:
            combined = combined + cf * (1 - combined)

        elif combined <= 0 and cf <= 0:
            combined = combined + cf * (1 + combined)

        else:
            denominator = 1 - min(abs(combined), abs(cf))

            if denominator == 0:
                combined = 0.0
            else:
                combined = (
                    combined + cf
                ) / denominator

    return round(combined, 4)


def certainty_percentage(factors):
    """Convert combined CF into a percentage estimate."""
    cf = calculate_certainty(factors)
    return round(max(0, cf) * 100, 2)
