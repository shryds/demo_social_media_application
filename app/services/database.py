import logging
import os

from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker , declarative_base
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

Base=declarative_base()
DATABASE_URL = os.environ.get("DATABASE_URL")
engine= create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.scalar()
        logger.info("Database connection established (PostgreSQL version: %s)", version)
except Exception as e:
    logger.error("Database connection failed: %s", e)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()