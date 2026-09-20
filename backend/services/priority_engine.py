def get_priority(cv_status, hydro_valid, confidence, data_completeness):
    if cv_status == "CONFLICT":
        return "P1", "Evidence conflict detected between field photo and satellite trends."
    if not hydro_valid:
        return "P1", "Hydrological validity failure: structure not on modeled drainage line."
    if confidence < 0.5:
        return "P1", "Very low confidence requires immediate field verification."
    
    if data_completeness < 1.0:
        return "P2", "Incomplete evidence (missing field photo)."
    if confidence < 0.75:
        return "P2", "Medium confidence requires routine review."
        
    return "P3", "Evidence is consistent, high confidence, no immediate verification signal."
