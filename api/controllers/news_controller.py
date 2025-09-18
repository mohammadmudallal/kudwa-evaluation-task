import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import pandas as pd
from fastapi import HTTPException, Response 
from fastapi.responses import JSONResponse
from utils.config.db.models import CompanyNews
from utils.config.db.migration import engine, session
from sqlalchemy import extract
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, timezone

class NewsController:
    def __init__(self):
        pass
    
    def latest_news(self, company_id: int, days: int = 1):
        try:
            days = int(days)

            today = datetime.now(timezone.utc).date()
            start_date = today - timedelta(days=days)

            start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
            end_dt = datetime.combine(today, datetime.max.time(), tzinfo=timezone.utc)

            # return Response(status_code=200, content=f"today: {today}, cuttof: {cutoff_date}")

            news = (
                session.query(CompanyNews)
                .options(joinedload(CompanyNews.company))
                .filter(CompanyNews.company_id == company_id)
                .filter(CompanyNews.datetime >= start_dt)
                .filter(CompanyNews.datetime <= end_dt)
                .order_by(CompanyNews.datetime.desc())
                .all()
            )

            if not news:
                raise HTTPException(
                    status_code=404,
                    detail=f"No news found for company {company_id} in the last {days} days",
                )

            news_json = [
                {
                    "id": n.id,
                    "company": n.company.name,
                    "headline": n.headline,
                    "summary": n.summary,
                    "datetime": n.datetime.isoformat(),
                    "source": n.source,
                    "image": n.image,
                    "category": n.category,
                }
                for n in news
            ]

            return JSONResponse(status_code=200, content=news_json)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))