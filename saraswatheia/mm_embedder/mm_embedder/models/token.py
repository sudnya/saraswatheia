# models.py
from sqlalchemy import Column, Integer, String, Table
from mm_embedder.database.database import get_metadata, get_declarative_base


from pydantic import BaseModel
# Pydantic model for data validation and serialization
Base = get_declarative_base()

class Token(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models



class TokenDB(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

tokenDb = Table('token', get_metadata(), 
                Column('id', Integer, primary_key=True),
                Column('name', String(50))
)

