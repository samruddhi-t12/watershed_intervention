from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.domain import InterventionDB

router = APIRouter()

@router.get("/api/v1/dashboard/metrics")
def get_metrics(db: Session = Depends(get_db)):
    all_invs = db.query(InterventionDB).all()
    total = len(all_invs)
    check_dams = len([i for i in all_invs if i.type == "Check Dam"])
    field_evidence = len([i for i in all_invs if not i.flag_missing_photo])
    needs_review = len([i for i in all_invs if i.status_badge == "REVIEW"])
    verified = len([i for i in all_invs if i.status_badge == "VERIFIED"])
    flagged = len([i for i in all_invs if i.status_badge == "FLAGGED"])
    
    return {
        "total": total,
        "check_dams": check_dams,
        "field_evidence": field_evidence,
        "needs_review": needs_review,
        "verified": verified,
        "flagged": flagged,
        "satellite_coverage": 1 if any(i.data_status == "DEMO" or i.data_status == "REAL" for i in all_invs) else 0
    }
