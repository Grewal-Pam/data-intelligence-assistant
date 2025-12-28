from typing import Dict, List

INTENT_REGISTRY: Dict[str, Dict] = {
    "bmi_change": {
        "description": "BMI change between baseline and follow-up visits",
        "query_file": "bmi_change.sql",
        "required_params": []
    },
    "bp_by_smoking": {
        "description": "Average blood pressure grouped by smoking status",
        "query_file": "bp_by_smoking.sql",
        "required_params": ["smoking_status"]
    },
    "sleep_by_education": {
        "description": "Average sleep duration by education level",
        "query_file": "sleep_by_education.sql",
        "required_params": []
    },
    "bmi_change_by_participant": {
    "query_file": "bmi_change_by_participant.sql",
    "required_params": ["participant_id"]
    }

}
