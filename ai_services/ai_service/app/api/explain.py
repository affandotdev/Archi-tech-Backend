# from app.core.cost_engine import calculate_cost
# from app.llm.gemini_client import generate_response
# from app.llm.prompts import explain_cost_prompt
# from app.schemas.estimate import EstimateRequest
# from fastapi import APIRouter

# router = APIRouter()


# @router.post("/explain")
# def explain_estimate(payload: EstimateRequest):
#     estimate = calculate_cost(**payload.dict())
#     prompt = explain_cost_prompt(estimate)
#     explanation = generate_response(prompt)

#     return {"estimate": estimate, "explanation": explanation, "ai_assisted": True}


# from app.schemas.estimate import ChatRequest


# @router.post("/chat")
# def chat_with_ai(payload: ChatRequest):
#     response = generate_response(payload.prompt)
#     return {"message": response, "ai_assisted": True}



# from fastapi import APIRouter
# from app.core.cost_engine import calculate_cost
# from app.core.rag_retriever import retrieve_relevant_rules, build_rag_context

# from app.llm.prompts import explain_cost_prompt
# from app.llm.gemini_client import generate_response


# router = APIRouter(prefix="/ai", tags=["AI"])




# def explain_with_rag(payload: dict):
#     cost = calculate_cost(**payload)

#     # 1. Build semantic query
#     query = "construction cost related to parking, safety, height, access"

#     # 2. Retrieve rules
#     rules = retrieve_relevant_rules(query, k=3)

#     # 3. Build RAG context
#     rag_context = build_rag_context(rules)

#     # 4. Build final prompt
#     prompt = explain_cost_prompt(
#         cost_data=cost,
#         regulations=rag_context
#     )

#     # 5. Gemini explains ONLY
#     explanation = generate_response(prompt)

#     return {
#         "estimate": cost,
#         "explanation": explanation,
#         "rules_used": [r["rule"] for r in rules],
#         "ai_assisted": True,
#     }


from fastapi import APIRouter

from app.core.cost_engine import calculate_cost
from app.core.rag_retriever import retrieve_relevant_rules, build_rag_context
from app.llm.prompts import explain_cost_prompt
from app.llm.gemini_client import generate_response
from app.core.rag_retriever import (
    retrieve_relevant_rules,
    build_rag_context,
    format_rules_for_client,
)



router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/explain")
def explain(payload: dict):
    cost = calculate_cost(**payload)

    query = "construction cost related to parking, safety, height, access"
    rules = retrieve_relevant_rules(query, k=3)
    rag_context = build_rag_context(rules)

    prompt = explain_cost_prompt(
        cost_data=cost,
        regulations=rag_context
    )

    explanation = generate_response(prompt)
    client_rules = format_rules_for_client(rules)
    return {
        "estimate": cost,
        "explanation": explanation,
        "rag_evidence": client_rules,
        "ai_assisted": True
    }
