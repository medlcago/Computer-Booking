from sqlalchemy import Column, String, BIGINT, MetaData, INTEGER
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Computer(Base):
    __tablename__ = 'computers'

    id: int = Column(BIGINT, primary_key=True, index=True)
    brand: str = Column(String(length=255), nullable=False)
    model: str = Column(String(length=255), nullable=False)
    cpu: str = Column(String(length=255), nullable=False)
    ram: int = Column(INTEGER, nullable=False)
    storage: int = Column(INTEGER, nullable=False)
    gpu: str = Column(String(length=255), nullable=False)
    description: str = Column(String(length=255), default=None)
    category: str = Column(String(length=255), nullable=False)
