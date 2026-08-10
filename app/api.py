from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.coordinator import coordinate_request


app = FastAPI(
    title="Vehicle Maintenance Agent",
    description=(
        "Agentic AI system for vehicle diagnosis "
        "and risk assessment"
    ),
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST MODEL
# ============================================================

class VehicleRequest(BaseModel):
    symptoms: str


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Vehicle Maintenance Agent API is running"
    }


# ============================================================
# DIAGNOSIS ENDPOINT
# ============================================================

@app.post("/diagnose")
def diagnose_vehicle(
    request: VehicleRequest
):

    result = coordinate_request(
        request.symptoms
    )

    return {
        "symptoms": request.symptoms,
        "result": result
    }