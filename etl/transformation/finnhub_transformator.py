import pandas as pd
import json as jn

from utils.logger.logger import Logger

class FinnhubTransformator:
    def __init__(self):
        with open("utils/config/data_config/finnhub_config.json", "r") as f:
            self.config = jn.load(f)
        self.logger = Logger()
        
    def remove_nulls(self, df):
        try:
            df = df.dropna(axis=1)
            return df
        except Exception as e:
            self.logger.log_error(f"Error in removing nulls: {e}")
            raise
        
    