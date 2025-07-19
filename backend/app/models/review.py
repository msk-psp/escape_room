from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .cafe import Base
import datetime

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    cafe_id = Column(Integer, ForeignKey('cafes.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=False)
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    cafe = relationship("Cafe", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
