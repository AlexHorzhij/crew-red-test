from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.projects.repository import ProjectRepository
from app.projects import schemas
from app.places.service import PlaceService


class ProjectService:
    @staticmethod
    def create_project(db: Session, project_in: schemas.ProjectCreate):
        # Validate places if present
        validated_places = []
        if project_in.places:
            if len(project_in.places) > 10:
                raise HTTPException(
                    status_code=400, detail="Project cannot have more than 10 places"
                )

            seen_ids = set()
            for p in project_in.places:
                if p.external_id in seen_ids:
                    raise HTTPException(
                        status_code=400, detail=f"Duplicate place ID {p.external_id}"
                    )
                seen_ids.add(p.external_id)
                # Just validate existence during project creation
                details = PlaceService.get_and_validate_artwork(p.external_id)
                validated_places.append(details)

        project_data = {
            "name": project_in.name,
            "description": project_in.description,
            "start_date": project_in.start_date,
        }
        try:
            db_project = ProjectRepository.create_project(
                db, project_data, commit=False
            )

            # Add places using PlaceService logic but more directly to avoid multiple API calls if cached
            # For simplicity here, we re-use the validated details
            from app.places.repository import PlaceRepository as PlaceRepo

            for details in validated_places:
                PlaceRepo.create_place(
                    db,
                    {
                        "project_id": db_project.id,
                        "external_id": details["id"],
                        "title": details["title"],
                    },
                    commit=False,
                )

            db.commit()
            db.refresh(db_project)
            return db_project
        except Exception as e:
            from app.core.logging_config import logger

            logger.error(f"Transaction failed during project creation: {e}")
            db.rollback()
            raise

    @staticmethod
    def get_project(db: Session, project_id: int):
        db_project = ProjectRepository.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        return db_project

    @staticmethod
    def list_projects(db: Session, skip: int = 0, limit: int = 100):
        return ProjectRepository.get_projects(db, skip, limit)

    @staticmethod
    def update_project(
        db: Session, project_id: int, project_update: schemas.ProjectUpdate
    ):
        db_project = ProjectRepository.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        update_data = project_update.dict(exclude_unset=True)
        return ProjectRepository.update_project(db, db_project, update_data)

    @staticmethod
    def delete_project(db: Session, project_id: int):
        db_project = ProjectRepository.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Validation: cannot delete if any place is visited
        if any(p.visited for p in db_project.places):
            raise HTTPException(
                status_code=400, detail="Cannot delete project with visited places"
            )

        return ProjectRepository.delete_project(db, db_project)

    @staticmethod
    def add_place_to_project(db: Session, project_id: int, external_id: int):
        db_project = ProjectRepository.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")

        if len(db_project.places) >= 10:
            raise HTTPException(
                status_code=400, detail="Project cannot have more than 10 places"
            )

        if any(p.external_id == external_id for p in db_project.places):
            raise HTTPException(
                status_code=400, detail="Place already exists in project"
            )

        return PlaceService.create_place(db, project_id, external_id)
