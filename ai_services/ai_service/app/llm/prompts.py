def explain_cost_prompt(cost_result: dict) -> str:
    return f"""
You are a construction cost assistant.
You must NOT change numbers.
You must NOT invent data.

Explain the following cost estimate to a client in simple terms.

Cost data:
{cost_result}

Focus on:
- what the cost means
- whether budget is enough
- risks and assumptions
"""
