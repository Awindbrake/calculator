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

# Define the milestone names and their corresponding durations
milestone_names = [
    "Engineering",
    "Deliveries",
    "Erection",
    "Technical Assistance",
    "Commercial Start-up (First Product)",
    "PAC",
    "FAC",
    "End of Warranty"
]

# Define the representatives' commission structure
representatives = {
    "Boogen": [
        {"name": "Range1", "limit": 500000, "percent": 0.05},
        {"name": "Range2", "limit": 2000000, "percent": 0.04},
        {"name": "Range3", "limit": 5000000, "percent": 0.03},
        {"name": "Range4", "limit": 10000000, "percent": 0.02},
        {"name": "Range5", "limit": 1000000000, "percent": 0.015},
    ],
    "Eksal": [
        {"name": "Range1", "limit": 250000, "percent": 0.03},
        {"name": "Range2", "limit": 500000, "percent": 0.03},
        {"name": "Range3", "limit": 1000000, "percent": 0.03},
        {"name": "Range4", "limit": 2500000, "percent": 0.03},
        {"name": "Range5", "limit": 5000000, "percent": 0.03},
        {"name": "Range6", "limit": 1000000000, "percent": 0.03},
    ],
    "Rep_name 1": [
        {"name": "Range1", "limit": 500000, "percent": 0.0167},
        {"name": "Range2", "limit": 2500000, "percent": 0.01},
        {"name": "Range3", "limit": 10000000, "percent": 0.004},
        {"name": "Range4", "limit": 25000000, "percent": 0.0023},
        {"name": "Range5", "limit": 1000000000, "percent": 0.0017},
    ],
    "Rep_name 2": [
        {"name": "Range1", "limit": 500000, "percent": 0.0167},
        {"name": "Range2", "limit": 2500000, "percent": 0.01},
        {"name": "Range3", "limit": 10000000, "percent": 0.004},
        {"name": "Range4", "limit": 25000000, "percent": 0.0023},
        {"name": "Range5", "limit": 1000000000, "percent": 0.0017},
    ],
    "Tuna": [
        {"name": "Range1", "limit": 50000, "percent": 0.07},
        {"name": "Range2", "limit": 150000, "percent": 0.06},
        {"name": "Range3", "limit": 1000000, "percent": 0.05},
        {"name": "Range4", "limit": 2000000, "percent": 0.04},
        {"name": "Range5", "limit": 3750000, "percent": 0.02},
    ],
    "Beyer": [
        {"name": "Range1", "limit": 500000, "percent": 0.05},
        {"name": "Range2", "limit": 2500000, "percent": 0.03},
        {"name": "Range3", "limit": 10000000, "percent": 0.012},
        {"name": "Range4", "limit": 25000000, "percent": 0.007},
        {"name": "Range5", "limit": 1000000000, "percent": 0.005},
    ],
    "Mak Demir": [
        {"name": "Range1", "limit": 500000, "percent": 0.045},
        {"name": "Range2", "limit": 5000000, "percent": 0.035},
        {"name": "Range3", "limit": 10000000, "percent": 0.02},
        {"name": "Range4", "limit": 1000000000, "percent": 0.01},
    ],
    "Meta Mak": [
        {"name": "Range1", "limit": 500000, "percent": 0.05},
        {"name": "Range2", "limit": 1000000, "percent": 0.04},
        {"name": "Range3", "limit": 2500000, "percent": 0.035},
        {"name": "Range4", "limit": 5000000, "percent": 0.025},
        {"name": "Range5", "limit": 1000000000, "percent": 0.015},
    ],
    "Tete": [
        {"name": "Range1", "limit": 300000, "percent": 0.05},
        {"name": "Range2", "limit": 1000000, "percent": 0.04},
        {"name": "Range3", "limit": 5000000, "percent": 0.03},
        {"name": "Range4", "limit": 10000000, "percent": 0.02},
        {"name": "Range5", "limit": 1000000000, "percent": 0.015},
    ],
    "JVO": [
        {"name": "Range1", "limit": 250000, "percent": 0.06},
        {"name": "Range2", "limit": 500000, "percent": 0.05},
        {"name": "Range3", "limit": 1000000, "percent": 0.04},
        {"name": "Range4", "limit": 1500000, "percent": 0.03},
        {"name": "Range5", "limit": 1000000000, "percent": 0.02},
    ],
    "Hotech": [
        {"name": "Range1", "limit": 500000, "percent": 0.05},
        {"name": "Range2", "limit": 1000000, "percent": 0.05},
        {"name": "Range3", "limit": 5000000, "percent": 0.035},
        {"name": "Range4", "limit": 10000000, "percent": 0.025},
        {"name": "Range5", "limit": 1000000000, "percent": 0.01},
    ],
    "Ilk San": [
        {"name": "Range1", "limit": 250000, "percent": 0.04},
        {"name": "Range2", "limit": 750000, "percent": 0.03},
        {"name": "Range3", "limit": 2500000, "percent": 0.02},
        {"name": "Range4", "limit": 1000000000, "percent": 0.01},
    ],
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
