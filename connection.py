from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.settings import settings

# For synchronous operations (Celery might need this, or we can use async with asyncio)
# FastAPI will use async if we change to async engine, but for simplicity of this setup we use sync sqlalchemy for now
# or we can use async. Let's use async for better performance.
# Need to replace postgresql:// with postgresql+asyncpg://
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# If using asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
