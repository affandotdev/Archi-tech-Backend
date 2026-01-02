def calculate_cost(
    plot_length_ft: float,
    plot_width_ft: float,
    floors: int,
    location: str,
    building_type: str,
    quality: str,
    budget_lakhs: float | None,
):
    base_cost_per_sqft = {
        "basic": 1600,
        "standard": 2000,
        "premium": 2600,
    }

    location_multiplier = {
        "city": 1.2,    # Metro/City
        "town": 1.0,    # Tier-2
        "village": 0.8, # Rural
    }

    built_up_area = plot_length_ft * plot_width_ft * floors * 0.8  

    cost_per_sqft = int(
        base_cost_per_sqft[quality]
        * location_multiplier.get(location.lower(), 1.0)
    )

    total_cost = (built_up_area * cost_per_sqft) / 100000  

    assumptions = [
        "Standard structural system",
        "No basement included",
        "No interior design costs",
        "Local labor rates applied",
    ]

    risks = []
    budget_status = None

    if budget_lakhs:
        budget_status = "within_budget" if total_cost <= budget_lakhs else "exceeds_budget"
        if total_cost > budget_lakhs:
            risks.append("Estimated cost exceeds provided budget")

    return {
        "total_area_sqft": round(built_up_area, 2),
        "cost_per_sqft": cost_per_sqft,
        "estimated_cost_lakhs": round(total_cost, 2),
        "budget_status": budget_status,
        "assumptions": assumptions,
        "risks": risks,
    }
