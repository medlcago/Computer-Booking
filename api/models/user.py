from sqlalchemy import Column, String, BIGINT, MetaData
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id: int = Column(BIGINT, primary_key=True, index=True)
    user_id: int = Column(BIGINT, nullable=False, unique=True)
    first_name: str = Column(String(length=255), nullable=False)
    last_name: str = Column(String(length=255), nullable=False)
    password: str = Column(String(length=255), nullable=False)
