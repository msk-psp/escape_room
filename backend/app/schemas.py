from pydantic import BaseModel
from typing import List, Optional
import datetime

from pydantic import BaseModel
from typing import List, Optional
import datetime

class Cafe(BaseModel):
    id: int
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    open_date: Optional[datetime.date]

    class Config:
        orm_mode = True

class Theme(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class Review(BaseModel):
    id: int
    cafe_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime.datetime

    class Config:
        orm_mode = True
