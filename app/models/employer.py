"""
A module for employer in the app-models package.
"""

from typing import TYPE_CHECKING

from pydantic import EmailStr, PositiveInt
from sqlalchemy import CheckConstraint, Integer
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.job import Job


class Employer(Base):  # type: ignore
    """
    User model class representing the "employer" table
    """

    __tablename__ = "employer"

    id: Mapped[PositiveInt] = mapped_column(
        Integer,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="ID of the employer",
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(200),
        nullable=False,
        comment="Name to identify the employer",
    )
    contact_email: Mapped[EmailStr] = mapped_column(
        VARCHAR(320),
        nullable=False,
        index=True,
        unique=True,
        comment="Preferred e-mail address of the employer",
    )
    industry: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        comment="Industry from the employer works",
    )
    jobs: Mapped[list["Job"]] = relationship(
        "Job",
        back_populates="employer",
        lazy="joined",
    )

    __table_args__ = (
        CheckConstraint("char_length(name) >= 4", name="employer_name_length"),
        CheckConstraint(
            "char_length(contact_email) >= 3",
            name="employer_contact_email_length",
        ),
        CheckConstraint(
            sql_database_setting.DB_EMAIL_CONSTRAINT,
            name="employer_email_format",
        ),
    )
