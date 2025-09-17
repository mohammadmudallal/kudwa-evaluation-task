import yfinance as yf
import pandas as pd
from utils.logger.logger import Logger

class PyFinanceExtractor:
    def __init__(self):
        self.logger = Logger()
    
    def fetch_data(self, ticker: str) -> pd.DataFrame:
        try:
            df = yf.download(ticker)
            df['source'] = 'yfinance'
            self.logger.log_info(f"Successfully fetched data for {ticker}")
            return df
        except Exception as e:
            self.logger.log_error(f"Failed to fetch data for {ticker}: {e}")
            return pd.DataFrame()
        
    def fetch_fx_rates(self, pairs: list[str] = None) -> pd.DataFrame:
        if pairs is None:
            # default popular pairs
            pairs = ["EURUSD=X", "GBPUSD=X", "JPY=X", "AUDUSD=X", "CADUSD=X", "CHFUSD=X", "NZDUSD=X"]
        
        data = []
        for pair in pairs:
            try:
                df = yf.download(pair, period="1d")
                if not df.empty:
                    data.append({
                        "CurrencyPair": pair.replace("=X", ""),
                        "Rate": df['Close'].iloc[-1],
                        "Date": df.index[-1].strftime("%Y-%m-%d %H:%M:%S")
                    })
                    self.logger.log_info(f"Fetched {pair} rate: {df['Close'].iloc[-1]}")
            except Exception as e:
                self.logger.log_error(f"Error fetching {pair}: {e}")
        
        return pd.DataFrame(data)
