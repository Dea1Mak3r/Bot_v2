from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from database import Base

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    status_code = Column(Integer, nullable=False)  # snake_case
    status_desc = Column(Text, nullable=False)     # snake_case
    timestamp = Column(TIMESTAMP(timezone=False), nullable=False)
    stand = Column(String(50), nullable=False)

class Version(Base):
    __tablename__ = "version"
    id = Column(Integer, primary_key=True, index=True)
    stand = Column(String(50), nullable=False)
    version = Column(String(10), nullable=False)