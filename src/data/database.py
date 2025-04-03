from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config folder
env_path = Path(__file__).parent.parent.parent / 'config' / '.env'
load_dotenv(env_path)

# Database configurations
SOURCE_DATABASE_URL = os.getenv(
    "SOURCE_DATABASE_URL",
    "postgresql+asyncpg://user:password@source-db:5432/source_db"
)
APP_DATABASE_URL = os.getenv(
    "APP_DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/app_db"
)

# Create async engines
source_engine = create_async_engine(SOURCE_DATABASE_URL, echo=True)
app_engine = create_async_engine(APP_DATABASE_URL, echo=True)

# Create async sessions
SourceSession = sessionmaker(
    source_engine, class_=AsyncSession, expire_on_commit=False
)
AppSession = sessionmaker(
    app_engine, class_=AsyncSession, expire_on_commit=False
)

# Create base classes for models
SourceBase = declarative_base()
AppBase = declarative_base()


async def get_source_session() -> AsyncSession:
    """Get source database session."""
    async with SourceSession() as session:
        yield session


async def get_app_session() -> AsyncSession:
    """Get application database session."""
    async with AppSession() as session:
        yield session


async def init_app_db():
    """Initialize application database tables."""
    async with app_engine.begin() as conn:
        await conn.run_sync(AppBase.metadata.create_all) 