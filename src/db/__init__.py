from conn import async_engine
from schema import Base


async def create_table_if_not_exists():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def check_table_exists():
    async with async_engine.begin() as conn:
        result = await conn.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'qa_data')"
        )
        return result.scalar()
