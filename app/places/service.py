from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.places.repository import PlaceRepository
from app.places import schemas
from app.external.art_api import get_artwork_details


from app.core.logging_config import logger


class PlaceService:
    @staticmethod
    def get_and_validate_artwork(external_id: int):
        return get_artwork_details(external_id)

    @classmethod
    def create_place(cls, db: Session, project_id: int, external_id: int):
        details = cls.get_and_validate_artwork(external_id)
        place_data = {
            "project_id": project_id,
            "external_id": details["id"],
            "title": details["title"],
        }
        return PlaceRepository.create_place(db, place_data)

    @staticmethod
    def update_place(db: Session, place_id: int, place_update: schemas.PlaceUpdate):
        db_place = PlaceRepository.get_place(db, place_id)
        if not db_place:
            raise HTTPException(status_code=404, detail="Place not found")

        update_data = place_update.dict(exclude_unset=True)
        return PlaceRepository.update_place(db, db_place, update_data)

    @staticmethod
    def get_place(db: Session, place_id: int):
        db_place = PlaceRepository.get_place(db, place_id)
        if not db_place:
            raise HTTPException(status_code=404, detail="Place not found")
        return db_place

    @staticmethod
    def list_places(query: str = "", skip: int = 0, limit: int = 50):
        try:
            # Convert skip to page (Art Institute uses 1-based paging)
            page = (skip // limit) + 1
            from app.external.art_api import search_artworks

            return search_artworks(query=query, page=page, limit=limit)
        except Exception as e:
            logger.error(f"Error listing places from external API: {e}")
            raise
