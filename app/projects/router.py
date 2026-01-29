from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.projects.service import ProjectService
from app.projects import schemas
from app.core.database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post(
    "/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED
)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return ProjectService.create_project(db, project)


@router.get("/", response_model=List[schemas.ProjectOut])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProjectService.list_projects(db, skip, limit)


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    return ProjectService.get_project(db, project_id)


@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    return ProjectService.update_project(db, project_id, project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    ProjectService.delete_project(db, project_id)
    return None


@router.post(
    "/{project_id}/places",
    response_model=schemas.PlaceOut,
    status_code=status.HTTP_201_CREATED,
)
def add_place_to_project(
    project_id: int, place_in: schemas.PlaceCreateInput, db: Session = Depends(get_db)
):
    return ProjectService.add_place_to_project(db, project_id, place_in.external_id)


@router.get("/{project_id}/places")
def read_project_places(project_id: int, db: Session = Depends(get_db)):
    project = ProjectService.get_project(db, project_id)
    return project.places
