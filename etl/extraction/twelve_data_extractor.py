import finnhub
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from utils.logger.logger import Logger
from twelvedata import TDClient


load_dotenv()

class TwelveDataExtractor:
    def __init__(self, api_key=os.getenv("TWELVE_DATA_API_KEY")):
        self.td = TDClient(apikey=api_key)
        self.logger = Logger()
        
    def fetch_exchange_rates(self,):
        try:
            symbols = ["USD/EUR", "USD/GBP", "USD/JPY", "EUR/GBP"]
            exchange_rates = []
            for symbol in symbols:
                response = self.td.exchange_rate(symbol=symbol).as_json()
                exchange_rates.append(response)
                
            return exchange_rates
        except Exception as e:
            self.logger.log_error(f"Error fetching exchange rates: {e}")
            
        
