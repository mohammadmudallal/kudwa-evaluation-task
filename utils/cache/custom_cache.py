import json as jn
import os
from pathlib import Path

class CustomCache:
    def __init__(self, annual_cache_file=os.getenv("ANNUAL_CACHE_FILE_PATH"), quarterly_cache_file=os.getenv("QUARTERLY_CACHE_FILE_PATH")):
        self.annual_cache_file = Path(annual_cache_file)
        self.quarterly_cache_file = Path(quarterly_cache_file)
        
    def create_cache(self):
        try:
            if not self.annual_cache_file.exists() or self.annual_cache_file.stat().st_size == 0:
                with open(self.annual_cache_file, "w") as f:
                    jn.dump({}, f)

            if not self.quarterly_cache_file.exists() or self.quarterly_cache_file.stat().st_size == 0:
                with open(self.quarterly_cache_file, "w") as f:
                    jn.dump({}, f)
                    
        except Exception as e:
            print(f"Error creating cache: {e}")
        
    def read_cache(self, is_annaul=True):
        try:
            with open(self.annual_cache_file if is_annaul else self.quarterly_cache_file, "r") as f:
                data = jn.load(f)
                
            return data
        except Exception as e:
            print(f"Error reading cache: {e}")
            return {}
        
    def write_cache(self, data, is_annaul=True):
        try:
            with open(self.annual_cache_file if is_annaul else self.quarterly_cache_file, "w") as f:
                jn.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing to cache: {e}")
            return False