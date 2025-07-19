from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import db, models, schemas

router = APIRouter()

@router.get("/", response_model=List[schemas.Theme])
def get_themes(
    name: Optional[str] = None,
    db: Session = Depends(db.get_db)
):
    query = db.query(models.Theme)
    if name:
        query = query.filter(models.Theme.name.ilike(f"%{name}%"))
    themes = query.all()
    return themes

@router.get("/{theme_id}", response_model=schemas.Theme)
def get_theme(theme_id: int, db: Session = Depends(db.get_db)):
    theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")
    return theme

@router.get("/{theme_id}/reviews", response_model=List[schemas.Review])
def get_theme_reviews(theme_id: int, db: Session = Depends(db.get_db)):
    theme = db.query(models.Theme).filter(models.Theme.id == theme_id).first()
    if theme is None:
        raise HTTPException(status_code=404, detail="Theme not found")

    cafe_ids = db.query(models.CafeTheme.cafe_id).filter(models.CafeTheme.theme_id == theme_id).all()
    cafe_ids = [c[0] for c in cafe_ids]

    reviews = db.query(models.Review).filter(models.Review.cafe_id.in_(cafe_ids)).all()
    return reviews
