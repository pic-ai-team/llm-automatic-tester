from sqlalchemy import Column, Integer, String, Text, ARRAY
from sqlalchemy.orm import DeclarativeBase


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
