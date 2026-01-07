from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import Literal


class EstimateRequest(BaseModel):
    plot_length_ft: float
    plot_width_ft: float
    floors: int

    location: Literal["city", "town", "village"]
    building_type: Literal["house", "apartment", "villa"]
    quality: Literal["basic", "standard", "premium"]

    budget_lakhs: float


class EstimateResponse(BaseModel):
    total_area_sqft: float
    estimated_cost_lakhs: float
    assumptions: List[str]
    risks: List[str]


class ChatRequest(BaseModel):
    prompt: str
