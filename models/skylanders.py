from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    skylander_name = Column(String, index=True)
    timestamp = Column(DateTime)