import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
from fastapi import HTTPException, Response 
from fastapi.responses import JSONResponse
from utils.config.db.models import ExchangeRates
from utils.config.db.migration import engine, session

class FxRatesController:
    def __init__(self):
        pass
        
    def latest_fx_rates(self, currency: str):
        try:
            rates = session.query(ExchangeRates).filter(ExchangeRates.symbol.ilike(f"{currency.upper().strip()}%")).all()
            
            if not rates:
                raise HTTPException(status_code=404, detail="No rates found for the specified currency")
            
            rates_json = [
                {
                    "symbol": r.symbol,
                    "rate": r.rate,
                    "created_at": r.created_at.isoformat()
                }
                for r in rates
            ]
            
            return JSONResponse(status_code=200, content=rates_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))