import os

files = {
    "backend/routers/layers.py": """from fastapi import APIRouter
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
""",
    "backend/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import dashboard, interventions, admin, layers
from backend.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIH26015 MVP - GIS Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(interventions.router)
app.include_router(admin.router)
app.include_router(layers.router)

@app.get("/health")
def health():
    return {"status": "ok"}
"""
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Backend updated.")
