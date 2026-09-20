def process_field_evidence(intervention):
    return {
        "has_photo": intervention.field_has_photo,
        "water_presence": intervention.field_water_presence,
        "vegetation": intervention.field_vegetation,
        "image_quality": intervention.field_image_quality,
        "geofence_valid": intervention.field_geofence_valid
    }
