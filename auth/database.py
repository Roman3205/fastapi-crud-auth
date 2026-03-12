from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(getenv("DB_URI"))

AsyncSessionLocal = async_sessionmaker(autoflush=False, autocommit=False, bind=engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

Base = declarative_base()