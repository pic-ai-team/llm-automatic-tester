import os
from typing import List
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Text, ARRAY, select
from sqlalchemy.orm import DeclarativeBase
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


class Base(DeclarativeBase):
    pass


class QAData(Base):
    __tablename__ = "qa_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)  # input
    answer = Column(Text, nullable=False)  # gt
    type = Column(String, nullable=False)  # evaluation type
    document = Column(Text, nullable=True)  # context document, can be None
    parser_type = Column(
        Text, nullable=True
    )  # type of parser used for parsing the document
    milvus_documents_ids = Column(ARRAY(Integer), nullable=True)  # milvus document IDs


async def create_table_if_not_exists():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_qa(
    question: str,
    answer: str,
    type: str,
    document: str = None,
    milvus_documents_ids: List[int] = None,
):
    new_entry = QAData(
        question=question,
        answer=answer,
        type=type,
        document=document,
        milvus_documents_ids=milvus_documents_ids,
    )
    session_maker = get_sessionmaker()
    async with session_maker() as session:
        session.add(new_entry)
        await session.commit()
        print(f"Entry created with ID: {new_entry.id}")
    return new_entry.id


async def read_all_qa():
    session_maker = get_sessionmaker()
    async with session_maker() as session:
        result = await session.execute(select(QAData))  # Await the execute method
        entries = result.scalars().all()  # Call scalars() on the result
    return entries


async def update_qa(
    entry_id,
    question=None,
    answer=None,
    type=None,
    document=None,
    milvus_documents_ids=None,
):
    session_maker = get_sessionmaker()
    async with session_maker() as session:
        entry = (
            await session.execute(select(QAData).where(QAData.id == entry_id))
        ).scalar_one_or_none()
        if not entry:
            print(f"Entry with ID {entry_id} not found.")
            return
        if question:
            entry.question = question
        if answer:
            entry.answer = answer
        if type:
            entry.type = type
        if document:
            entry.document = document
        if milvus_documents_ids:
            entry.milvus_documents_ids = milvus_documents_ids
        await session.commit()
        print(f"Entry with ID {entry_id} updated successfully.")


async def delete_qa(entry_id):
    session_maker = get_sessionmaker()
    async with session_maker() as session:
        entry = (
            await session.execute(select(QAData).where(QAData.id == entry_id))
        ).scalar_one_or_none()
        if not entry:
            print(f"Entry with ID {entry_id} not found.")
            return
        await session.delete(entry)
        await session.commit()
        print(f"Entry with ID {entry_id} deleted successfully.")


# Example Usage
if __name__ == "__main__":
    import asyncio

    async def main():
        start_id = 231294000
        document_ids = [start_id + i for i in range(69)]
        entries = await read_all_qa()
        for entry in entries:
            if entry.document == "ADAM":
                print("update entry with id:", entry.id)
                await update_qa(entry_id=entry.id, milvus_documents_ids=document_ids)
            print(
                f"ID: {entry.id}, Question: {entry.question}, Answer: {entry.answer}, Type: {entry.type}, Document: {entry.document}"
            )

    asyncio.run(main())
