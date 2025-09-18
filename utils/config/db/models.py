from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    metrics = relationship("Metric", back_populates="company")
    annual_series = relationship("AnnualSeries", back_populates="company")
    quarterly_series = relationship("QuarterlySeries", back_populates="company")
    news = relationship("CompanyNews", back_populates="company")



class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    metric_type = Column(String(255), nullable=False)
    metric_value = Column(Float, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="metrics")


class AnnualSeries(Base):
    __tablename__ = "annual_series"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    metric_name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    period = Column(Date, nullable=False)
    pct_change = Column(Float, nullable=True)
    ma_2 = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="annual_series")


class QuarterlySeries(Base):
    __tablename__ = "quarterly_series"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    metric_name = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    period = Column(Date, nullable=False)
    pct_change = Column(Float, nullable=True)
    ma_4 = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="quarterly_series")
    
    
class CompanyNews(Base):
    __tablename__ = "company_news"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    category = Column(String(50), nullable=True)
    headline = Column(String(500), nullable=True)
    summary = Column(String(2000), nullable=True)
    source = Column(String(100), nullable=True)
    url = Column(String(1000), nullable=True)
    image = Column(String(1000), nullable=True)
    related = Column(String(255), nullable=True)
    datetime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="news")
    

class ExchangeRates(Base):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
class ExchangeRatesArchive(Base):
    __tablename__ = "exchange_rates_archive"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(50), nullable=False)
    rate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)