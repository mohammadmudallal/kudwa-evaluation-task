from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from utils.config.db.models import Base, Company
import os

load_dotenv()

db_name = os.getenv("MYSQL_DB")
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_port = os.getenv("MYSQL_PORT")

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/")

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.commit()

engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def seed_companies():
    companies = [
        {"symbol": "AAPL", "name": "Apple"},
        # {"symbol": "MSFT", "name": "Microsoft"},
        # {"symbol": "GOOGL", "name": "Alphabet"},
    ]

    for data in companies:
        existing = session.query(Company).filter_by(symbol=data["symbol"]).first()
        if not existing:
            company = Company(symbol=data["symbol"], name=data["name"])
            session.add(company)
            print(f"Inserted {data['symbol']} - {data['name']}")
        else:
            print(f"Skipped {data['symbol']} (already exists)")

    session.commit()
    
seed_companies()
