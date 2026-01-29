from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.places.service import PlaceService
from app.places import schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/places",
    tags=["places"],
)


@router.get("/", response_model=schemas.PlaceExternalOut)
def list_places(skip: int = 0, limit: int = 50):
    return PlaceService.list_places(skip=skip, limit=limit)


@router.get("/{place_id}", response_model=schemas.PlaceOut)
def read_place(place_id: int, db: Session = Depends(get_db)):
    return PlaceService.get_place(db, place_id)


@router.put("/{place_id}", response_model=schemas.PlaceOut)
def update_place(
    place_id: int, place: schemas.PlaceUpdate, db: Session = Depends(get_db)
):
    return PlaceService.update_place(db, place_id, place)
