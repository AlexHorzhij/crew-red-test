from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from app.places.schemas import PlaceOut, PlaceCreateInput


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreateInput]] = []


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectOut(ProjectBase):
    id: int
    places: List[PlaceOut] = []
    is_completed: bool

    class Config:
        orm_mode = True
