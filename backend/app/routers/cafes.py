from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Cafe])
def get_cafes(
    region: Optional[str] = None,
    name: Optional[str] = None,
    db: Session = Depends(db.get_db)
):
    query = db.query(models.Cafe)
    if region:
        query = query.filter(models.Cafe.address.ilike(f"%{region}%"))
    if name:
        query = query.filter(models.Cafe.name.ilike(f"%{name}%"))
    cafes = query.all()
    return cafes

@router.get("/{cafe_id}", response_model=schemas.Cafe)
def get_cafe(cafe_id: int, db: Session = Depends(db.get_db)):
    cafe = db.query(models.Cafe).filter(models.Cafe.id == cafe_id).first()
    if cafe is None:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return cafe
