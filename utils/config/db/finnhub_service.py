from utils.config.db.migration import engine, session
from utils.config.db.models import Metric, Company, CompanyNews
from utils.logger.logger import Logger
from datetime import datetime

class FinnhubService:
    def __init__(self, session=session):
        self.session = session
        self.logger = Logger()
    
    def get_all_companies(self):
        try:
            companies = session.query(Company).all()
            return companies
        except Exception as e:
            self.session.rollback()
            self.logger.log_error(f"Error Fetching companies table: {e}")
            raise
        
    def truncate_metrics(self):
        try:
            num_deleted = self.session.query(Metric).delete()
            self.session.commit()
            self.logger.log_info(f"Truncated Metrics table, deleted {num_deleted} records.")
        except Exception as e:
            self.session.rollback()
            self.logger.log_error(f"Error truncating Metrics table: {e}")
            raise
        
    def create_news_item(self, item, company_id):
        try:
            if "datetime" in item and isinstance(item["datetime"], (int, float)):
                item["datetime"] = datetime.fromtimestamp(item["datetime"])
            
            item["company_id"] = company_id
            del item["id"]
            
            self.session.add(CompanyNews(**item))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.logger.log_error(f"Error adding news item: {e}")
            raise