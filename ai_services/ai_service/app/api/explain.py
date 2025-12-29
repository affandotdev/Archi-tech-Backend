from fastapi import APIRouter
from app.core.cost_engine import calculate_cost
from app.llm.gemini_client import generate_response
from app.llm.prompts import explain_cost_prompt
from app.schemas.estimate import EstimateRequest

router = APIRouter()

@router.post("/explain")
def explain_estimate(payload: EstimateRequest):
    estimate = calculate_cost(**payload.dict())
    prompt = explain_cost_prompt(estimate)
    explanation = generate_response(prompt)

    return {
        "estimate": estimate,
        "explanation": explanation,
        "ai_assisted": True
    }

from app.schemas.estimate import ChatRequest

@router.post("/chat")
def chat_with_ai(payload: ChatRequest):
    response = generate_response(payload.prompt)
    return {
        "message": response,
        "ai_assisted": True
    }

