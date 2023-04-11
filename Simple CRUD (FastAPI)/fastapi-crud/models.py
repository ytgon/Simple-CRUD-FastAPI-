from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Magician(Base):
    __tablename__ = 'magicians'
    id = Column(Integer, primary_key = True, index=True)
    fullname = Column(String)
    description = Column(String)
    