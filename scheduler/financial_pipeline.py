import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime, timedelta
import pandas as pd
import time
import json
import re

from etl.extraction.finnhub_extractor import FinnhubExtractor
from etl.transformation.finnhub_transformator import FinnhubTransformator
from etl.load.finnhub_loader import FinnhubLoader

from etl.extraction.pyfinance_extractor import PyFinanceExtractor

from utils.helpers.write_to_csv import write_to_csv
from utils.helpers.camel_to_readable import camel_to_readable
from utils.logger.logger import Logger
from utils.config.db.models import Metric, Company
from utils.config.db.migration import engine
from sqlalchemy.orm import sessionmaker

finnubh_extractor = FinnhubExtractor()
finnhub_transformator = FinnhubTransformator()
finnhub_loader = FinnhubLoader()

pyfinance_extractor = PyFinanceExtractor()

logger = Logger()
Session = sessionmaker(bind=engine)
session = Session()


def save_finnhub_data(data, file_path="finnhub_data.json"):
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)  # pretty print with indent
        print(f"Data saved to {file_path}")
    except Exception as e:
        print(f"Error saving data: {e}")


def extract_finnhub_data():
    try:
        logger.log_info(f"[{datetime.now()}] Starting Finnhub extraction...")
        companies = session.query(Company).all()
        for company in companies:
            data = finnubh_extractor.fetch_company_basic_financials(
                symbol=company.symbol
            )
            metrics = []

            for metric_name, metric_value in data["metric"].items():
                metric_name_clean = camel_to_readable(metric_name)
                if isinstance(metric_value, str):
                    parsed_date = datetime.fromisoformat(metric_value)
                    metric_value = parsed_date.timestamp()

                metrics.append(
                    Metric(
                        company_id=company.id,
                        metric_type=metric_name_clean,
                        metric_value=metric_value,
                    )
                )

            finnhub_loader.load_data(metrics)

        # df = finnhub_transformator.validate_dtypes(df)
        # df = finnhub_transformator.remove_nulls(df)
        # logger.log_info("Successfully extracted data from Finnhub")
        # return df
    except Exception as e:
        logger.log_error(f"Error extracting data from Finnhub: {e}")


def extract_finnhub_news():
    try:
        logger.log_info(f"[{datetime.now()}] Starting Finnhub news extraction...")
        to_date = datetime.now().strftime("%Y-%m-%d")
        from_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        df = finnubh_extractor.fetch_company_news(
            symbol="AAPL", from_date=from_date, to_date=to_date
        )
        logger.log_info("Successfully extracted news data from Finnhub")
        path = write_to_csv(df, source="finnhub", prefix="AAPL_News")
        logger.log_info(f"Finnhub News CSV written to {path}")
        return df
    except Exception as e:
        logger.log_error(f"Error extracting news data from Finnhub: {e}")


def extract_pyfinance():
    try:
        logger.log_info(f"[{datetime.now()}] Starting PyFinance extraction...")
        ingestor = PyFinanceExtractor()
        df = pyfinance_extractor.fetch_data(
            ticker="^GSPC"
        )  # yfinance symbol for S&P 500
        path = write_to_csv(df, source="pyfinance", prefix="sp500")
        logger.log_info(f"PyFinance CSV saved")
    except Exception as e:
        logger.log_error(f"Error extracting data from PyFinance: {e}")


def extract_exchange_rates_pyfinance():
    try:
        logger.log_info(f"[{datetime.now()}] Starting PyFinance FX extraction...")
        df = pyfinance_extractor.fetch_fx_rates()  # fetch multiple pairs
        if not df.empty:
            path = write_to_csv(df, source="pyfinance", prefix="FX_Rates")
            logger.log_info(f"PyFinance FX CSV saved to {path}")
    except Exception as e:
        logger.log_error(f"Error extracting FX rates from PyFinance: {e}")


def run():
    while True:
        start = datetime.now()
        logger.log_info(f"ETL job started at {start}")
        # extract_finnhub_data()
        # extract_pyfinance()
        extract_finnhub_data()
        elapsed = (datetime.now() - start).total_seconds()
        logger.log_info(f"ETL job completed in {elapsed} seconds")
        # Wait until the next 1-minute mark
        sleep_time = max(0, 60 - elapsed)
        time.sleep(sleep_time)


if __name__ == "__main__":
    run()
