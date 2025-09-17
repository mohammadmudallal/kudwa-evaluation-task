from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from utils.config.db.models import Base
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
