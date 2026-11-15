
# MAFDES - Educational Knowledge Base
# All rules use fictional simulated indicators.

AIRCRAFT_RULES = [

    {
        "name": "RULE_01",
        "if": [
            "power_alert",
            "sensor_disagreement"
        ],
        "then": "power_status_uncertain",
        "description": "Multiple simulated indicators suggest an uncertain power-system status.",
        "cf": 0.85
    },

    {
        "name": "RULE_02",
        "if": [
            "cooling_alert",
            "temperature_warning"
        ],
        "then": "cooling_status_uncertain",
        "description": "Simulated cooling indicators require further review.",
        "cf": 0.80
    },

    {
        "name": "RULE_03",
        "if": [
            "data_alert",
            "sensor_disagreement"
        ],
        "then": "sensor_data_inconsistent",
        "description": "The simulated sensor readings are inconsistent.",
        "cf": 0.90
    },

    {
        "name": "RULE_04",
        "if": [
            "power_status_uncertain",
            "sensor_data_inconsistent"
        ],
        "then": "system_review_required",
        "description": "Multiple simulated alerts require an overall system review.",
        "cf": 0.90
    },

    {
        "name": "RULE_05",
        "if": [
            "all_checks_clear"
        ],
        "then": "simulation_status_normal",
        "description": "All selected simulated checks are clear.",
        "cf": 0.95
    }
]
