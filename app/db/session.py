from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/auramind.db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
