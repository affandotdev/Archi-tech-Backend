from typing import List, Optional

from app.core.cost_engine import calculate_cost
from app.schemas.estimate import EstimateRequest, EstimateResponse
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


@router.post("/estimate", response_model=EstimateResponse)
def estimate(req: EstimateRequest):
    result = calculate_cost(**req.dict())
    return result
