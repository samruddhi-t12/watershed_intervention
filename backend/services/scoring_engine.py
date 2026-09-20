def calculate_scores(field, sat, cv_status):
    impact = 0.25*sat['savi_trend'] + 0.25*sat['mndwi_trend'] + 0.20*0.5 + 0.15*sat['temporal_consistency'] + 0.15*field['water_presence']
    source_agreement = 1.0 if cv_status == "AGREEMENT" else (0.0 if cv_status == "CONFLICT" else 0.5)
    data_completeness = 1.0 if field['has_photo'] else 0.5
    confidence = 0.25*data_completeness + 0.20*field['image_quality'] + 0.20*0.8 + 0.20*source_agreement + 0.15*sat['cloud_free_ratio']
    return max(0, min(1, impact)), max(0, min(1, confidence))
