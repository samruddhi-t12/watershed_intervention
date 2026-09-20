from fastapi import FastAPI
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
