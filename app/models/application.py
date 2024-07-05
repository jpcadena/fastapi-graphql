"""
A module for application in the app-models package.
"""

from pydantic import PositiveInt
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.models.job import Job
from app.models.user import User


class Application(Base):  # type: ignore
    """
    User model class representing the "application" table
    """

    __tablename__ = "application"

    id: Mapped[PositiveInt] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="ID of the Application",
    )
    user_id: Mapped[PositiveInt] = mapped_column(
        Integer,
        ForeignKey(
            "users.id",
            name="users_id_fkey",
        ),
        nullable=False,
        comment="ID of the User",
    )
    job_id: Mapped[PositiveInt] = mapped_column(
        Integer,
        ForeignKey(
            "job.id",
            name="job_id_fkey",
        ),
        nullable=False,
        comment="ID of the Job",
    )
    user: Mapped["User"] = relationship(
        "User", back_populates="users", lazy="joined"
    )
    job: Mapped["Job"] = relationship(
        "Job", back_populates="job", lazy="joined"
    )
