from typing import List
from sqlalchemy import select

from conn import get_sessionmaker
from schema import QAData


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
        entries = await read_all_qa()
        for entry in entries:
            print(
                f"ID: {entry.id}, Question: {entry.question}, Answer: {entry.answer}, Type: {entry.type}, Document: {entry.document}"
            )

    asyncio.run(main())
