
# MAFDES - Simulated Knowledge Facts

def generate_facts(inputs):
    """
    Convert user-selected simulation indicators
    into facts for the expert system.
    """

    facts = []

    if inputs.get("power_alert", False):
        facts.append("power_alert")

    if inputs.get("sensor_disagreement", False):
        facts.append("sensor_disagreement")

    if inputs.get("cooling_alert", False):
        facts.append("cooling_alert")

    if inputs.get("temperature_warning", False):
        facts.append("temperature_warning")

    if inputs.get("data_alert", False):
        facts.append("data_alert")

    if not facts:
        facts.append("all_checks_clear")

    return facts


def get_all_indicators():
    """Return available simulated indicators."""

    return {
        "power_alert": "Power status alert",
        "sensor_disagreement": "Sensor data disagreement",
        "cooling_alert": "Cooling status alert",
        "temperature_warning": "Temperature status warning",
        "data_alert": "Data consistency alert"
    }
