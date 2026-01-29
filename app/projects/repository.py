from sqlalchemy.orm import Session
from app.core import models
from app.core.logging_config import logger


class ProjectRepository:
    @staticmethod
    def get_project(db: Session, project_id: int):
        return db.query(models.Project).filter(models.Project.id == project_id).first()

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Project).offset(skip).limit(limit).all()

    @staticmethod
    def create_project(db: Session, project_data: dict, commit: bool = True):
        try:
            db_project = models.Project(**project_data)
            db.add(db_project)
            if commit:
                db.commit()
                db.refresh(db_project)
            else:
                db.flush()
            return db_project
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            db.rollback()
            raise

    @staticmethod
    def update_project(db: Session, db_project: models.Project, update_data: dict):
        try:
            for key, value in update_data.items():
                setattr(db_project, key, value)
            db.add(db_project)
            db.commit()
            db.refresh(db_project)
            return db_project
        except Exception as e:
            logger.error(f"Error updating project {db_project.id}: {e}")
            db.rollback()
            raise

    @staticmethod
    def delete_project(db: Session, db_project: models.Project):
        try:
            db.delete(db_project)
            db.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting project {db_project.id}: {e}")
            db.rollback()
            raise
