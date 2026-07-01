from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# Using SQLite with the async driver aiosqlite
DATABASE_URL = "sqlite+aiosqlite:///./courses.db"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create the sessionmaker for async sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Declarative base model
Base = declarative_base()

# Dependency function to provide database sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
