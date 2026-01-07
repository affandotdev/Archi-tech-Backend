from datetime import datetime

from .client import db


async def save_estimate(
    request_payload: dict, cost_result: dict, explanation: str | None = None
):
    document = {
        "request": request_payload,
        "result": cost_result,
        "explanation": explanation,
        "created_at": datetime.utcnow(),
    }

    await db.cost_estimates.insert_one(document)
