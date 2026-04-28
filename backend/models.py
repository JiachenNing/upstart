from sqlalchemy import Column, Integer, String, Text
from database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    gender = Column(String, nullable=True)
    message = Column(Text)
