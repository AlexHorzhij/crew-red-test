from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    start_date = Column(Date, nullable=True)

    places = relationship(
        "Place", back_populates="project", cascade="all, delete-orphan"
    )

    @property
    def is_completed(self):
        if not self.places:
            return False
        return all(place.visited for place in self.places)


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    external_id = Column(Integer)  # Art Institute API uses integer IDs
    notes = Column(String, nullable=True)
    visited = Column(Boolean, default=False)

    # Optional: Cache some info from external API to make listing faster/easier
    title = Column(String, nullable=True)

    project = relationship("Project", back_populates="places")

    __table_args__ = (
        UniqueConstraint("project_id", "external_id", name="_project_place_uc"),
    )
