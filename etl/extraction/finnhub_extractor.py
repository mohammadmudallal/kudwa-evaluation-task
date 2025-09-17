import finnhub
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.logger.logger import Logger

load_dotenv()

class FinnhubExtractor:
    def __init__(self, api_key=os.getenv("FINNHUB_API_KEY")):
        self.client = finnhub.Client(api_key=api_key)
        self.logger = Logger()
        
    def fetch_company_basic_financials(self, symbol: str):
        try:
            self.logger.log_info(f"Fetching daily stock candles for {symbol}")
            data = self.client.company_basic_financials(symbol, "all")
            return data
        except Exception as e:
            self.logger.log_error(f"Error fetching daily stock candles for {symbol}: {e}")
            raise
        
    def fetch_company_news(self, symbol: str, from_date: str, to_date: str) -> pd.DataFrame:
        try:
            self.logger.log_info(f"Fetching company news for {symbol} from {from_date} to {to_date}")
            news = self.client.company_news(symbol, from_date, to_date)
            df = pd.DataFrame(news)
            df['symbol'] = symbol
            return df
        except Exception as e:
            self.logger.log_error(f"Error fetching company news for {symbol}: {e}")
            raise
