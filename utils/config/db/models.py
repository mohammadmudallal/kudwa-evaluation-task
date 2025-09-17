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
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    company = relationship("Company", back_populates="quarterly_series")
