from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session_marker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    try:
        async with async_session_marker() as session:
            yield session
    finally:
        await session.close()
