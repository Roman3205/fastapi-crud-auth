from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from os import getenv

load_dotenv()

engine = create_engine(getenv("DB_URI"))

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()