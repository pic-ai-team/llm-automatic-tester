import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

load_dotenv(override=True)

# Define the database connection
username = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
database = os.getenv("PG_DATABASE")

DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
async_engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    return async_session
