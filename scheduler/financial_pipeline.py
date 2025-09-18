import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta
import pandas as pd
import time
import json
import re
import json
from pathlib import Path
import schedule
import time

from etl.extraction.finnhub_extractor import FinnhubExtractor
from etl.transformation.finnhub_transformator import FinnhubTransformator
from etl.load.finnhub_loader import FinnhubLoader

from etl.extraction.twelve_data_extractor import TwelveDataExtractor

from etl.extraction.pyfinance_extractor import PyFinanceExtractor

from utils.helpers.write_to_csv import write_to_csv
from utils.helpers.camel_to_readable import camel_to_readable
from utils.logger.logger import Logger
from utils.config.db.models import Metric, Company, QuarterlySeries, AnnualSeries, CompanyNews
from utils.config.db.migration import engine
from utils.config.db.finnhub_service import FinnhubService
from utils.config.db.td_service import TdService
from utils.cache.custom_cache import CustomCache
from sqlalchemy.orm import sessionmaker

finnubh_extractor = FinnhubExtractor()
finnhub_transformator = FinnhubTransformator()
finnhub_loader = FinnhubLoader()
finnhub_service = FinnhubService()

td_extractor = TwelveDataExtractor()
td_service = TdService()

pyfinance_extractor = PyFinanceExtractor()

logger = Logger()
custom_cache = CustomCache()
Session = sessionmaker(bind=engine)
session = Session()

def map_record_to_orm(record, is_annual=True):
    if is_annual:
        return {
            "company_id": record["company_id"],
            "metric_name": record["metric"],
            "value": record["v"],
            "period": record["period"],
            "pct_change": record.get("pct_change"),
            "ma_2": record.get("ma_2")
        }
        
    return {
        "company_id": record["company_id"],
        "metric_name": record["metric"],
        "value": record["v"],
        "period": record["period"],
        "pct_change": record.get("pct_change"),
        "ma_4": record.get("ma_4"),
        "volatility": record.get("volatility")
    }

def extract_company_basic_financials():
    try:
        logger.log_info(f"[{datetime.now()}] Starting Finnhub extraction...")
        
        companies = finnhub_service.get_all_companies()
    
        for company in companies:
            data = finnubh_extractor.fetch_company_basic_financials(
                symbol=company.symbol
            )
            
            finnhub_service.truncate_metrics()
            
            metrics = []    
            for metric_name, metric_value in data["metric"].items():
                if isinstance(metric_value, str):
                    parsed_date = datetime.fromisoformat(metric_value)
                    metric_value = parsed_date.timestamp()

                metrics.append(
                    Metric(
                        company_id=company.id,
                        metric_type=metric_name,
                        metric_value=metric_value,
                    )
                )
                        
            created = custom_cache.create_cache()
            annual_cache_data = custom_cache.read_cache(is_annaul=True)
            quarterly_cache_data = custom_cache.read_cache(is_annaul=False)
            
            annual_enriched_data = finnhub_transformator.enrich_financial_series(
                series_data=data['series']["annual"].items(),
                cache_data=annual_cache_data,
                company_id=company.id,
                window=2
            )
            
            quarterly_enriched_data = finnhub_transformator.enrich_financial_series(
                series_data=data['series']["quarterly"].items(),
                cache_data=quarterly_cache_data,
                company_id=company.id,
                window=4
            )

            finnhub_loader.load_data(metrics)
            finnhub_loader.load_data(
                [QuarterlySeries(**map_record_to_orm(rec, is_annual=False)) for rec in quarterly_enriched_data]
            )
            finnhub_loader.load_data(
                [AnnualSeries(**map_record_to_orm(rec)) for rec in annual_enriched_data]
            )
    except Exception as e:
        logger.log_error(f"Error extracting data from Finnhub: {e}")

def extract_finnhub_news():
    try:
        companies = finnhub_service.get_all_companies()
        logger.log_info(f"[{datetime.now()}] Starting Finnhub news extraction...")
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        
        for company in companies:
            news = finnubh_extractor.fetch_company_news(
                symbol=company.symbol, from_date=from_date, to_date=to_date
            )
            
            for n in news:
                finnhub_service.create_news_item(n, company.id)
            
            logger.log_info(f"Inserted {len(news)} news items for {company.symbol}")
    except Exception as e:
        logger.log_error(f"Error extracting news data from Finnhub: {e}")

def extract_exchange_rates_forex():
    try:
        logger.log_info(f"[{datetime.now()}] Starting PyFinance FX extraction...")
        td_service.archive_rates()
        rates = td_extractor.fetch_exchange_rates()
        for rate in rates:
            del rate["timestamp"]
            td_service.create_exchange_rate(rate)
        logger.log_info(f"Inserted {len(rates)} exchange rates from TwelveData")
    except Exception as e:
        logger.log_error(f"Error extracting FX rates from PyFinance: {e}")

# schedule.every().day.at("00:00").do(extract_finnhub_news) 
schedule.every(1).minutes.do(extract_exchange_rates_forex) 
schedule.every(1).minutes.do(extract_company_basic_financials) 

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
