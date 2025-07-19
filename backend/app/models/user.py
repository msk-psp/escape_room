from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .cafe import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)

    reviews = relationship("Review", back_populates="user")
