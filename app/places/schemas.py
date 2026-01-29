from typing import Optional
from pydantic import BaseModel


class PlaceBase(BaseModel):
    external_id: int
    notes: Optional[str] = None
    visited: bool = False


class PlaceCreateInput(BaseModel):
    external_id: int


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    visited: Optional[bool] = None


class PlaceOut(PlaceBase):
    id: int
    project_id: int
    title: Optional[str] = None

    class Config:
        orm_mode = True


class PlaceItem(BaseModel):
    external_id: int
    title: Optional[str] = None


class PlaceExternalOut(BaseModel):
    items: list[PlaceItem]
    pagination: dict
