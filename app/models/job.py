"""
A module for job in the app-models package.
"""

from typing import TYPE_CHECKING

from pydantic import PositiveInt
from sqlalchemy import CheckConstraint, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.employer import Employer


class Job(Base):  # type: ignore
    """
    User model class representing the "employer" table
    """

    __tablename__ = "job"

    id: Mapped[PositiveInt] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="ID of the Job",
    )
    title: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Title to identify the job",
    )
    description: Mapped[str] = mapped_column(
        VARCHAR(320),
        nullable=False,
        comment="Description to identify the job",
    )
    employer_id: Mapped[PositiveInt] = mapped_column(
        Integer,
        ForeignKey(
            "employer.id",
            name="job_employer_id_fkey",
        ),
        nullable=False,
        comment="ID of the Employer related with the job",
    )
    employer: Mapped["Employer"] = relationship(
        "Employer",
        back_populates="jobs",
        lazy="joined",
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="job", lazy="joined"
    )

    __table_args__ = (
        CheckConstraint("char_length(title) >= 4", name="job_title_length"),
        CheckConstraint(
            "char_length(description) >= 5",
            name="job_description_length",
        ),
    )
