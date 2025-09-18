import pandas as pd
import json as jn
import numpy as np
from utils.helpers.cache_functions import read_cache, write_cache

from utils.logger.logger import Logger
from utils.cache.custom_cache import CustomCache

class FinnhubTransformator:
    def __init__(self):
        with open("utils/config/data_config/finnhub_config.json", "r") as f:
            self.config = jn.load(f)
        self.logger = Logger()
        self.custom_cache = CustomCache()
        
    def remove_nulls(self, df):
        try:
            df = df.dropna()
            return df
        except Exception as e:
            self.logger.log_error(f"Error in removing nulls: {e}")
            raise
        
    def transform_series(self, series_name, records, company_id, window=2):        
        df = pd.DataFrame(records) 
        df = df.sort_values("period") 
        
        df["pct_change"] = df["v"].pct_change() * 100
        df[f"ma_{window}"] = df["v"].rolling(window=window).mean()
        
        if window == 4:
            df['volatility'] = df['v'].rolling(window=window).std()
        
        df = df.replace([np.inf, -np.inf], np.nan)
        df = self.remove_nulls(df)
        
        df["metric"] = series_name
        df['company_id'] = company_id
        
        cache = self.custom_cache.read_cache(is_annaul=(window==2))
        cache[series_name] = df.tail(4).to_dict(orient="records")
        
        data_written = self.custom_cache.write_cache(cache,is_annaul=(window==2))
        
        if not data_written:
            self.logger.log_error("Failed to update cache after transformation.")
                    
        return df.to_dict(orient="records")   
    
    
    def transform_new_series(self, series_name, records, company_id, window=2):        
        cache = self.custom_cache.read_cache(is_annaul=(window==2))
        
        cached_records = cache.get(series_name, [])
        combined_records = cached_records + records
        combined_records = sorted(combined_records, key=lambda x: pd.to_datetime(x['period']))
        
        cache_size = len(cached_records)
        combined_records = combined_records[-cache_size:]
        
        return self.transform_series(series_name, combined_records, company_id, window)
    
    
    def enrich_financial_series(self, series_data, cache_data, company_id, window=2):
        enriched_data = []
        for metric, records in series_data:
            if metric in cache_data and cache_data[metric]:
                cached_dates = [pd.to_datetime(r['period']) for r in cache_data[metric]] 
                latest_cached = max(cached_dates)
                
                new_records = [ r for r in records if pd.to_datetime(r['period']) > latest_cached ]
                if new_records: 
                    enriched = self.transform_new_series(metric, new_records, company_id, window=4) 
                    enriched_data.extend(enriched)
            else:
                enriched = self.transform_series(metric, records, company_id, window)
                enriched_data.extend(enriched)
                
        return enriched_data

                            
                            
                            
