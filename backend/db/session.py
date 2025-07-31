from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.core.config import settings

engine = create_async_engine(settings.orm_conn_str)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)