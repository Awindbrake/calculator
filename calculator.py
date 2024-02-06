
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


class provided_data(TypedDict, total=False):
    contract_price: Optional[float]
    mark_up: Optional[float]
    
    

@app.post("/submitData")
def submit_data(input_data: provided_data):
    # Process the data
    # For example, you can pass this data to your calculation functions
    # and return the results
    return {"message": "Data received successfully"}


@app.post("/calculateKPIs")
def api_calculate_kpis(input_data: provided_data):
    kpi_results = {}
    try:
        # Iterate through each year's data in the input
        for year, details in input_data.data.items():
            # Calculate KPIs for this year
            kpis_for_year = calculate_kpis(details, year)
            kpi_results[year] = kpis_for_year
        return kpi_results
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

def calculate_kpis(input_data):
    try:
        # Retrieve values from financial_data, set defaults to 0 if not present
        contract_price = input_data.get('contract_price', 0)
        mark_up = financial_data.get('mark_up', 0)
        final_price = contract_price * (1+mark_up)


        # Perform calculations
        kpi_data = {
            'final price': contract_price * (1+mark_up) if mark_up else contract_price,
            
            
        }
        
        return kpi_data

    except TypeError as e:
        # Handle specific type error (e.g., if non-numeric value encountered)
        raise HTTPException(status_code=422, detail=f"Type error in financial data: {e}")
    except ZeroDivisionError:
        # Handle division by zero error specifically
        raise HTTPException(status_code=422, detail="Attempted to divide by zero in KPI calculations")
    except Exception as e:
        # Catch-all for any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error calculating KPIs: {str(e)}")



# Main function, assuming it's now being used to run a simple server
def main():
    
    
    # Placeholder for server start, actual server running code would be needed here
    pass

if __name__ == "__main__":
    main()

