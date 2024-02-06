from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError, Field
from typing import Optional

app = FastAPI(
    title="Commission Calculator",
    description="Calculates commissions based on contract amount and representative.",
    version="1.0.0",
    servers=[
        {
            "url": "https://pricecalculator-0a512b36a62f.herokuapp.com",
            "description": "Commission Calculator API"
        }
    ]
)

# Define the representatives' commission structure
representatives = {
    # Your existing representatives dictionary
}

class CommissionData(BaseModel):
    amount_to_calculate: float = Field(..., gt=0, description="The contract amount to calculate the commission for.")
    representative: str = Field(..., description="The name of the representative.")

def calculate_cumulative_commission(amount_to_calculate: float, representative: str) -> float:
    cumulative_commission = 0
    ranges = representatives.get(representative, [])
    previous_limit = 0

    for r in ranges:
        if amount_to_calculate > previous_limit:
            amount_in_range = min(amount_to_calculate - previous_limit, r["limit"] - previous_limit)
            cumulative_commission += amount_in_range * r["percent"]
            previous_limit = r["limit"]
        else:
            break
    return cumulative_commission

@app.post("/calculate_commission")
async def calculate_commission(data: CommissionData):
    if data.representative not in representatives:
        raise HTTPException(status_code=404, detail="Representative not found")
    commission = calculate_cumulative_commission(data.amount_to_calculate, data.representative)
    return {"representative": data.representative, "commission": commission}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Commission Calculator API. Visit /docs for documentation."}
