from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
import settings

DATABASE_URL = "postgresql+asyncpg://"+settings.PG_USER+\
                    ":"+settings.PG_PASSWORD+"@"+settings.PG_HOST+\
                    ":"+settings.PG_PORT+"/"+settings.PG_DBNAME

engine = create_async_engine(DATABASE_URL, echo=False)

Base = declarative_base()
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
async def init_model() -> None:
    async with engine.begin() as conn:
        print('Запущен механизм drop_all, create_all')
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

#Depends
async def get_session()-> AsyncSession:
    async with async_session() as session:
        yield session
async def session_destroy():
    await engine.dispose()