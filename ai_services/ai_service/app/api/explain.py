


from fastapi import APIRouter

from app.core.cost_engine import calculate_cost
from app.core.rag_retriever import retrieve_relevant_rules, build_rag_context
from app.llm.prompts import explain_cost_prompt, CONSULTANT_SYSTEM_PROMPT
from app.llm.ollama_client import generate_response
from app.core.rag_retriever import (
    retrieve_relevant_rules,
    build_rag_context,
    format_rules_for_client,
)



router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/explain")
def explain(payload: dict):
    try:
        cost = calculate_cost(**payload)

        query = "construction cost related to parking, safety, height, access"
        try:
            rules = retrieve_relevant_rules(query, k=5)
            rag_context = build_rag_context(rules)
        except Exception as e:
            # Fallback to empty context if RAG fails
            rag_context = "No specific regulations found."
            rules = []

        prompt = explain_cost_prompt(
            cost_data=cost,
            regulations=rag_context
        )

        try:
            explanation = generate_response(prompt, system=CONSULTANT_SYSTEM_PROMPT)
        except Exception as e:
            print(f"Ollama/AI Error: {e}")
            from app.core.fallback import generate_fallback_explanation
            explanation = generate_fallback_explanation(cost)
        
        client_rules = format_rules_for_client(rules)
        return {
            "estimate": cost,
            "explanation": explanation,
            "rag_evidence": client_rules,
            "ai_assisted": True
        }
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Internal Failure: {str(e)}")


@router.post("/chat")
def chat(payload: dict):
    try:
        prompt = payload.get("prompt")
        if not prompt:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Prompt is required")

        # Use the consultant system prompt for consistent persona
        response = generate_response(prompt, system=CONSULTANT_SYSTEM_PROMPT)
        
        # Frontend expects 'message' key to avoid stringifying the whole JSON
        return {"message": response}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"AI Chat Error: {str(e)}")
