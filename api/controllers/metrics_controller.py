import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
from fastapi import HTTPException, Response 
from fastapi.responses import JSONResponse
from utils.config.db.models import Metric, AnnualSeries, QuarterlySeries
from utils.config.db.migration import engine, session
from utils.helpers.camel_to_readable import camel_to_readable
from sqlalchemy import extract
from sqlalchemy.orm import joinedload

class MetricsController:
    def __init__(self):
        pass
    
    def get_company_metrics(self, company_id: int):
        try:
            metrics = session.query(Metric).filter(Metric.company_id == company_id).all()
            
            if not metrics:
                raise HTTPException(status_code=404, detail="No metrics found for the specified company ID")
            
            metrics_json = [
                {
                    "id": m.id,
                    "company_id": m.company_id,
                    "metric_name": camel_to_readable(m.metric_type),
                    "value": m.metric_value,
                    "created_at": m.created_at.isoformat()
                }
                for m in metrics
            ]
            
            return JSONResponse(status_code=200, content=metrics_json)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def get_company_annaul_metrics(self, company_id: int, from_year: int, to_year: int):
        try:
            annual_metrics = (
                session.query(AnnualSeries)
                .options(joinedload(AnnualSeries.company))
                .filter(AnnualSeries.company_id == company_id)
                .filter(extract("year", AnnualSeries.period) >= from_year)
                .filter(extract("year", AnnualSeries.period) <= to_year)
                .all()
            )

            if not annual_metrics:
                raise HTTPException(
                    status_code=404,
                    detail=f"No annual metrics found for company {company_id} between {from_year} and {to_year}",
                )

            return [
                {
                    "id": m.id,
                    "company": m.company.name,
                    "period": m.period.isoformat(),
                    "metric": camel_to_readable(m.metric_name),
                    "moving_avg": m.ma_2,
                    "percentage_change": m.pct_change,
                    "value": m.value,
                }
                for m in annual_metrics
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_company_quartely_metrics(self, company_id: int, from_year: int, to_year: int):
        try:
            annual_metrics = (
                session.query(QuarterlySeries)
                .options(joinedload(QuarterlySeries.company))
                .filter(QuarterlySeries.company_id == company_id)
                .filter(extract("year", QuarterlySeries.period) >= from_year)
                .filter(extract("year", QuarterlySeries.period) <= to_year)
                .all()
            )

            if not annual_metrics:
                raise HTTPException(
                    status_code=404,
                    detail=f"No annual metrics found for company {company_id} between {from_year} and {to_year}",
                )

            return [
                {
                    "id": m.id,
                    "company": m.company.name,
                    "period": m.period.isoformat(),
                    "metric": camel_to_readable(m.metric_name),
                    "moving_avg": m.ma_4,
                    "percentage_change": m.pct_change,
                    "volatility": m.volatility,
                    "value": m.value,
                }
                for m in annual_metrics
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))    
        