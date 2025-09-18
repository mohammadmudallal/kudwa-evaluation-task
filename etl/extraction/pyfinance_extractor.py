import yfinance as yf
import pandas as pd
from utils.logger.logger import Logger

class PyFinanceExtractor:
    def __init__(self):
        self.logger = Logger()
    
    def fetch_data(self, ticker: str) -> pd.DataFrame:
        try:
            df = yf.download(ticker)
            self.logger.log_info(f"Successfully fetched data for {ticker}")
            return df
        except Exception as e:
            self.logger.log_error(f"Failed to fetch data for {ticker}: {e}")
            return pd.DataFrame()
        
    def fetch_fx_rates(self, pairs=None):
        if pairs is None:
            pairs = ["EURUSD=X", "GBPUSD=X", "JPY=X", "AUDUSD=X", "CADUSD=X", "CHFUSD=X", "NZDUSD=X"]

        columns = ["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]
        records = []

        for pair in pairs:
            try:
                df = yf.download(pair, period="1d")
                if df.empty:
                    continue
                df.reset_index(inplace=True)
                for _, row in df.iterrows():
                    record = {
                        "Ticker": pair,
                        "Date": row["Date"],
                        "Open": row["Open"],
                        "High": row["High"],
                        "Low": row["Low"],
                        "Close": row["Close"],
                        "Volume": row["Volume"]
                    }
                    records.append(record)
            except Exception as e:
                print(f"Error fetching {pair}: {e}")

        return pd.DataFrame(records, columns=columns)