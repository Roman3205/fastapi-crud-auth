from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from os import getenv
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(getenv("DB_URI"))

AsyncSessionLocal = async_sessionmaker(autoflush=True, bind=engine, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    pass