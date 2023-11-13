from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import config

engine = create_async_engine(url=config.db.db_url)
async_session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_db() -> AsyncSession:
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()
