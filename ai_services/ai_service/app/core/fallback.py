def generate_fallback_explanation(cost_data):
    """
    Generates a deterministic explanation for the cost estimate
    when the AI service is unavailable.
    """
    total_lakhs = cost_data.get("estimated_cost_lakhs", 0)
    area = cost_data.get("total_area_sqft", 0)
    rate = cost_data.get("cost_per_sqft", 0)
    status = cost_data.get("budget_status")
    
    explanation = f"""
### Cost Estimate Summary

Based on your requirements, the estimated construction cost is **₹{total_lakhs} Lakhs**.

**Breakdown:**
*   **Total Built-up Area**: {area} sq.ft.
*   **Estimated Rate**: ₹{rate}/sq.ft.

This calculation considers standard material costs and local labor rates.
"""

    if status == "within_budget":
        explanation += "\n\n**Budget Analysis**: Good news! This estimate is within your specified budget."
    elif status == "exceeds_budget":
        explanation += "\n\n**Budget Analysis**: This estimate currently exceeds your specified budget. You might consider reducing the floor area or adjusting the finish quality."

    explanation += """

## Critical Safety & Awareness
1. **Soil Test**: Mandatory before foundation work to determine load-bearing capacity.
2. **Structural Audit**: Ensure your structural drawings are vetted by a certified engineer.
3. **Labor Insurance**: Verify all workers on site are insured against accidents.
4. **Permits**: Obtain all necessary KMBR/KPBR approvals before breaking ground.
"""

    explanation += "\n\n> *Note: This is an automated estimate generated while our AI advisory service is temporarily unavailable.*"
    
    return explanation
