from pydantic import BaseModel
from typing import Optional, List
from fastapi import APIRouter
from app.schemas.estimate import EstimateRequest, EstimateResponse
from app.core.cost_engine import calculate_cost

router = APIRouter()


@router.post("/estimate", response_model=EstimateResponse)
def estimate(req: EstimateRequest):
    result = calculate_cost(**req.dict())
    return result
