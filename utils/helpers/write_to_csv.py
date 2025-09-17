from datetime import datetime
from pathlib import Path
import pandas as pd
from utils.logger.logger import Logger

logger = Logger()

def write_to_csv(df: pd.DataFrame, source: str, prefix: str):
    outdir = Path("artifacts") / source
    outdir.mkdir(parents=True, exist_ok=True)
    
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')  # replace ":" with "-"
    filename = outdir / f"{prefix}_{ts}.json"
    
    df.to_json(filename, orient='records')
    logger.log_info(f"✅ Data written to {filename}")
    return str(filename)
