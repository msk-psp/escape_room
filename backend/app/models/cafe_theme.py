from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .cafe import Base

class CafeTheme(Base):
    __tablename__ = 'cafe_themes'

    cafe_id = Column(Integer, ForeignKey('cafes.id'), primary_key=True)
    theme_id = Column(Integer, ForeignKey('themes.id'), primary_key=True)

    cafe = relationship("Cafe", back_populates="themes")
    theme = relationship("Theme", back_populates="cafes")
