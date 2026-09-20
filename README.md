# Watershed Intervention Evidence Engine

**An intervention-level geospatial decision-support layer for watershed development monitoring.**

Built to extend existing watershed-monitoring infrastructure with automated, cross-validated evidence interpretation — not to replace it.

[**Live Application**](https://watershed-intervention.vercel.app/)

---

## Overview

Watershed interventions — check dams, farm ponds, contour trenches, plantations — are typically monitored through geo-tagged field photographs and satellite imagery collected independently, then interpreted manually. This creates two problems: field evidence is filed as documentation rather than structured data, and satellite trends are read in isolation, without controlling for rainfall or seasonal variation.

This system addresses both by automatically cross-validating field and satellite evidence for each intervention, producing a transparent, auditable score and a prioritized verification queue for field officers.

## Core Capabilities

| Capability | Description |
|---|---|
| Field evidence extraction | Zero-shot photo classification (CLIP) combined with classical computer vision signals — no custom model training required |
| Satellite time-series analysis | SAVI (vegetation) and MNDWI (water) indices tracked across multiple time points per intervention |
| Reference-zone comparison | Each site's change is compared against a buffer zone of matching land cover, isolating genuine intervention impact from seasonal or rainfall-driven change |
| Hydrological validity check | A DEM-derived stream network confirms whether a structure is actually sited on a real drainage line, computed from real elevation and catchment data |
| Evidence cross-validation | Disagreement between field-photo evidence and satellite-derived evidence is explicitly flagged rather than averaged away |
| Impact and Confidence scoring | Two independent, component-transparent scores — high apparent impact with low confidence is never reported as a verified success |
| Prioritized verification queue | Interventions ranked by evidence status (Flagged / Needs Review / Verified) with a stated reason for each ranking |

## Navigating the Application

The application opens on the **Overview** tab, showing summary statistics for the current project.

- **Interventions tab** — a searchable, priority-sorted queue of all interventions on the left. Selecting an entry opens the Intervention Inspector on the right, with four sub-tabs: Overview (scores), Evidence (field photo and record metadata), Change (satellite trend data), and Flags (any validity or conflict issues detected).
- **Change Detection tab** — a full-coverage analytical grid over the watershed boundary. Use the timeline control to move between monitoring periods, and the layer toggles on the left to switch between Vegetation (SAVI), Water Conservation (MNDWI), and the Integrated Change Index.
- **Analytics tab** — aggregate charts across all interventions: priority distribution, confidence distribution, and evidence agreement rates.
- **Demo Mode toggle** (top right) — this application distinguishes real, computed geospatial data (watershed boundary, elevation model, stream network) from illustrative prototype data (multi-year vegetation/water trend values, some intervention records), since real multi-year satellite time-series were not available for this prototype. Toggling Demo Mode on populates the interface with internally consistent illustrative data so the full workflow can be evaluated end to end; every layer using this data is marked with a visible **Synthetic** indicator regardless of whether Demo Mode is on. Toggling it off shows only genuine, unfabricated records, including cases explicitly marked "coordinates unavailable" where no real data exists.
- **Data Sources** (top right) — a reference panel listing exactly which layers in the application are computed from real data versus illustrative prototype data, with citations.
- **Generate Report** (top right) — produces a downloadable PDF summary of the current project's interventions and findings.

## Data Provenance

| Layer | Source | Status |
|---|---|---|
| Watershed boundary | OpenStreetMap | Real |
| Elevation model | SRTM 30m, via OpenTopography | Real |
| Stream network & catchment | Derived from the above via `pysheds` (fill → flow direction → flow accumulation → stream extraction → catchment delineation) | Real, computed |
| Hydrological validity check | Computed against the real stream network above | Real |
| Field-record schema | Modeled on a real government geo-tagged field-photo record structure, for interoperability | Real schema, prototype data |
| Vegetation / water trend values (SAVI, MNDWI) | — | Illustrative (Demo Mode) |

Full detail is available in-app via the Data Sources panel.

## Technology Stack

**Application**
Python · JavaScript · React · Leaflet · FastAPI

**Geospatial processing**
Rasterio · GDAL · pysheds · OpenTopography (elevation data)

**Computer vision**
CLIP (zero-shot classification) · OpenCV

**Analytics**
NumPy · Pandas · scikit-learn

**Data & reporting**
SQLite · GeoJSON · jsPDF

## Running Locally

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend — optional, only required for regenerating the underlying data
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

The deployed build is fully static: all geospatial and intervention data is pre-computed and shipped as static JSON/GeoJSON files under `frontend/public/data`, so the deployed application runs without a live backend.

## Project Structure

- backend/ FastAPI backend (local development / data generation only)
- data/ Raw and processed geospatial data (elevation model, boundary, streams)
- frontend/ React application (deployed as a static site)
- offline_scripts/ One-time data processing pipeline (elevation fetch, hydrology, analytical grid generation)
- scripts/ Utility scripts

