from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .cafe import Base

class Theme(Base):
    __tablename__ = 'themes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    cafes = relationship("CafeTheme", back_populates="theme")
