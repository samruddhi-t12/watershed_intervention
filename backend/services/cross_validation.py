def validate_evidence(field, sat):
    # Mock logic based on demo scenarios
    if field['has_photo'] and field['water_presence'] > 0.5 and sat['mndwi_trend'] < 0:
        return "CONFLICT"
    elif field['has_photo'] and field['water_presence'] > 0.5 and sat['mndwi_trend'] > 0:
        return "AGREEMENT"
    else:
        return "INCONCLUSIVE"
