
import pandas as pd
import base64
import requests
import pandas as pd
import io
from io import StringIO
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from typing import Dict, TypedDict, Optional



app = FastAPI(
        title = "calculator",
        description = "Performs financial analysis and calculates various KPIs based on submitted financial data.",
        version = "1.0.0",
        servers = [
            {

            "url": "https://pricecalculator-0a512b36a62f.herokuapp.com",
            "description": "calculator"
            }
        ]
            )

@app.get("/")
def read_root():
    return """
    <html>
        <head>
            <title>FastAPI Application</title>
        </head>
        <body>
            <h1>Welcome to the FastAPI application!</h1>
            <p>Visit <a href="/docs">/docs</a> for the API documentation.</p>
        </body>
    </html>
    """


class FinancialData(BaseModel):
    contract_price: float
    mark_up: float

@app.post("/calculateKPIs")
def api_calculate_kpis(input_data: FinancialData):
    try:
        kpi_results = calculate_kpis(input_data.dict())
        return kpi_results
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

def calculate_kpis(input_data):
    try:
        # Retrieve values from input_data
        contract_price = input_data.get('contract_price', 0)
        mark_up = input_data.get('mark_up', 0)

        # Perform calculations
        final_price = contract_price * (1 + mark_up)

        kpi_data = {
            'final_price': final_price,
        }
        
        return kpi_data
    except Exception as e:
        # Handle any unexpected errors during calculation
        raise Exception(f"Error in KPI calculation: {e}")


# Main function, assuming it's now being used to run a simple server
def main():
    
    
    # Placeholder for server start, actual server running code would be needed here
    pass

if __name__ == "__main__":
    main()

