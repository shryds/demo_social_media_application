from sqlalchemy import create_engine,text
from sqlalchemy.orm import declarative_base

Base=declarative_base()

DATABASE_URL = "postgresql://postgres:postgres@localhost/something"

engine= create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("Connection successful! PostgreSQL version:")
        for row in result:
            print(row[0])
except Exception as e:
    print(f"Connection failed: {e}")