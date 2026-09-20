from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, Boolean
from backend.database import Base

class InterventionDB(Base):
    __tablename__ = "interventions"
    id = Column(Integer, primary_key=True, index=True)
    work_code = Column(String, index=True)
    type = Column(String)
    data_status = Column(String) # REAL, DEMO, UNAVAILABLE
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    
    score_impact = Column(Float, nullable=True)
    score_confidence = Column(Float, nullable=True)
    priority = Column(String)
    status_badge = Column(String)
    priority_reason = Column(String)
    
    impact_veg = Column(Float, nullable=True)
    impact_water = Column(Float, nullable=True)
    impact_lulc = Column(Float, nullable=True)
    impact_temporal = Column(Float, nullable=True)
    impact_field = Column(Float, nullable=True)
    
    ndvi_change = Column(Float, nullable=True)
    mndwi_change = Column(Float, nullable=True)
    water_spread_change = Column(Float, nullable=True)
    
    ref_ndvi_change = Column(Float, nullable=True)
    ref_mndwi_change = Column(Float, nullable=True)
    rainfall_context = Column(String, nullable=True)
    cv_signal_text = Column(String, nullable=True)
    
    cost_estimated = Column(Integer, nullable=True)
    
    flag_hydro = Column(Boolean, default=False)
    flag_water = Column(Boolean, default=False)
    flag_veg = Column(Boolean, default=False)
    flag_season = Column(Boolean, default=False)
    flag_conflict = Column(Boolean, default=False)
    flag_missing_photo = Column(Boolean, default=True)
    
    # DRISHTI fields
    drishti_sl_no = Column(Integer, nullable=True)
    drishti_server_time = Column(String, nullable=True)
    drishti_apptype = Column(String, nullable=True)
    drishti_appsubtype = Column(String, nullable=True)
    drishti_fdcprojectname = Column(String, nullable=True)
    drishti_themename = Column(String, nullable=True)
    drishti_profilename = Column(String, nullable=True)
    drishti_observername = Column(String, nullable=True)
    drishti_org = Column(String, nullable=True)
    drishti_mobileno = Column(String, nullable=True)
    drishti_creationtime = Column(String, nullable=True)
    drishti_uuid = Column(String, nullable=True)
    drishti_deviceid = Column(String, nullable=True)
    drishti_name = Column(String, nullable=True)
    drishti_statusofactivity = Column(String, nullable=True)
    drishti_location = Column(String, nullable=True)
    drishti_datecompletion = Column(String, nullable=True)
    drishti_details = Column(String, nullable=True)

class InterventionSchema(BaseModel):
    id: int
    work_code: str
    type: str
    data_status: str
    lat: Optional[float]
    lng: Optional[float]
    score_impact: Optional[float]
    score_confidence: Optional[float]
    priority: str
    status_badge: str
    priority_reason: str
    impact_veg: Optional[float]
    impact_water: Optional[float]
    impact_lulc: Optional[float]
    impact_temporal: Optional[float]
    impact_field: Optional[float]
    ndvi_change: Optional[float] = None
    mndwi_change: Optional[float] = None
    water_spread_change: Optional[float] = None
    ref_ndvi_change: Optional[float] = None
    ref_mndwi_change: Optional[float] = None
    rainfall_context: Optional[str] = None
    cv_signal_text: Optional[str] = None
    cost_estimated: Optional[int] = None
    flag_hydro: bool
    flag_water: bool
    flag_veg: bool
    flag_season: bool
    flag_conflict: bool
    flag_missing_photo: bool
    
    drishti_sl_no: Optional[int] = None
    drishti_server_time: Optional[str] = None
    drishti_apptype: Optional[str] = None
    drishti_appsubtype: Optional[str] = None
    drishti_fdcprojectname: Optional[str] = None
    drishti_themename: Optional[str] = None
    drishti_profilename: Optional[str] = None
    drishti_observername: Optional[str] = None
    drishti_org: Optional[str] = None
    drishti_mobileno: Optional[str] = None
    drishti_creationtime: Optional[str] = None
    drishti_uuid: Optional[str] = None
    drishti_deviceid: Optional[str] = None
    drishti_name: Optional[str] = None
    drishti_statusofactivity: Optional[str] = None
    drishti_location: Optional[str] = None
    drishti_datecompletion: Optional[str] = None
    drishti_details: Optional[str] = None
    
    class Config:
        from_attributes = True
