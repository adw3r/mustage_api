from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.config import DB_URI

engine = create_async_engine(url=DB_URI)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
