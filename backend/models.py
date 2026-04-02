from sqlalchemy import Column, Integer, String
from backend.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    summary = Column(String)
    embedding = Column(String)
    tags = Column(String)
