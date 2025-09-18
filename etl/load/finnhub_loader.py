from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from utils.config.db.migration import engine
from utils.logger.logger import Logger

class FinnhubLoader:
    def __init__(self):
        self.logger = Logger()    
        self.engine = engine
        self.session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        
    def load_data(self, data):
        session: Session = self.session()
        try:
            session.add_all(data)  # <-- use add_all instead of bulk_save_objects
            session.commit()
            self.logger.log_info(f"Successfully inserted {len(data)} records into DB.")
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.log_error(f"Error loading data to destination: {e}")
            raise
        except Exception as e:
            self.logger.log_error(f"Error loading data to destination: {e}")
            raise
        finally:
            session.close()
