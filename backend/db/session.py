from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.core.config import settings

# Ensure the DATABASE_URL uses asyncpg
engine = create_async_engine(settings.db_url, echo=True)

# Create the session factory for async sessions
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency for FastAPI routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
