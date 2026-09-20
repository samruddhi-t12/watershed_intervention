from fastapi import APIRouter
import subprocess
import os

router = APIRouter()

@router.post("/api/v1/admin/reset")
def reset_db():
    script_path = os.path.join(os.path.dirname(__file__), "../../scripts/generate_demo_data.py")
    subprocess.run(["python", script_path], check=True)
    return {"status": "success", "message": "Database reset to deterministic demo state."}
