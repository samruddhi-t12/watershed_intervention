def process_satellite_evidence(intervention):
    return {
        "savi_trend": intervention.sat_savi_trend,
        "mndwi_trend": intervention.sat_mndwi_trend,
        "temporal_consistency": intervention.sat_temporal_consistency,
        "cloud_free_ratio": intervention.sat_cloud_free_ratio
    }
