from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()
DATA_DIR = os.path.join(os.path.dirname(__file__), "../../data/geojson")

@router.get("/api/v1/layers/{layer_name}")
def get_layer(layer_name: str):
    file_path = os.path.join(DATA_DIR, f"{layer_name}.geojson")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "Layer not found"}
