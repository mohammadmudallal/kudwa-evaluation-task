from utils.config.db.migration import engine, session
from utils.config.db.models import ExchangeRates, ExchangeRatesArchive
from utils.logger.logger import Logger
from datetime import datetime


class TdService:
    def __init__(self, session=session):
        self.session = session
        self.logger = Logger()

    def create_exchange_rate(self, rate):
        try:
            self.session.add(ExchangeRates(**rate))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.logger.log_error(f"Error adding exchange rate: {e}")
            raise

    def archive_rates(self):
        try:
            rates = self.session.query(ExchangeRates).all()
            
            if len(rates) > 0:
                for rate in rates:
                    archive = ExchangeRatesArchive(
                        symbol=rate.symbol,
                        rate=rate.rate,
                        created_at=rate.created_at,
                        updated_at=rate.updated_at
                    )
                    self.session.add(archive)
                    self.session.delete(rate)

                self.session.commit()

        except Exception as e:
            self.session.rollback()
            self.logger.log_error(f"Error archiving exchange rates: {e}")
            raise
