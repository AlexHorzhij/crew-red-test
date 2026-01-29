from sqlalchemy.orm import Session
from app.core import models
from app.core.logging_config import logger


class PlaceRepository:
    @staticmethod
    def get_place(db: Session, place_id: int):
        return db.query(models.Place).filter(models.Place.id == place_id).first()

    @staticmethod
    def create_place(db: Session, place_data: dict, commit: bool = True):
        try:
            db_place = models.Place(**place_data)
            db.add(db_place)
            if commit:
                db.commit()
                db.refresh(db_place)
            else:
                db.flush()
            return db_place
        except Exception as e:
            logger.error(f"Error creating place: {e}")
            db.rollback()
            raise

    @staticmethod
    def update_place(db: Session, db_place: models.Place, update_data: dict):
        try:
            for key, value in update_data.items():
                setattr(db_place, key, value)
            db.add(db_place)
            db.commit()
            db.refresh(db_place)
            return db_place
        except Exception as e:
            logger.error(f"Error updating place {db_place.id}: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_places(db: Session, skip: int = 0, limit: int = 50):
        return db.query(models.Place).offset(skip).limit(limit).all()
