from sqlalchemy import Column, Integer, String, Double, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class Cafe(Base):
    __tablename__ = 'cafes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
    geom = Column(Geometry('POINT'))

    reviews = relationship("Review", back_populates="cafe")
    themes = relationship("CafeTheme", back_populates="cafe")
