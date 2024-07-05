"""
A module for user in the app models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import EmailStr, PositiveInt
from sqlalchemy import CheckConstraint, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.application import Application


class User(Base):  # type: ignore
    """
    User model class representing the "users" table
    """

    __tablename__ = "users"

    id: Mapped[PositiveInt] = mapped_column(
        INTEGER,
        nullable=False,
        primary_key=True,
        index=True,
        unique=True,
        comment="ID of the User",
    )
    username: Mapped[str] = mapped_column(
        VARCHAR(15),
        index=True,
        unique=True,
        nullable=False,
        comment="Username to identify the user",
    )
    email: Mapped[EmailStr] = mapped_column(
        VARCHAR(320),
        index=True,
        unique=True,
        nullable=False,
        comment="Preferred e-mail address of the User",
    )
    hashed_password: Mapped[str] = mapped_column(
        VARCHAR(97), nullable=False, comment="Hashed password of the User"
    )
    role: Mapped[str] = mapped_column(
        VARCHAR(50), nullable=False, comment="Role of the User"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the User was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        nullable=True,
        onupdate=text("now()"),
        comment="Time the User was updated",
    )
    applications: Mapped[list["Application"]] = relationship(
        "Application", back_populates="user", lazy="joined"
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(username) >= 4",
            name="users_username_length",
        ),
        CheckConstraint(
            "char_length(email) >= 3",
            name="users_email_length",
        ),
        CheckConstraint(
            sql_database_setting.DB_EMAIL_CONSTRAINT[8:],
            name="users_email_format",
        ),
        CheckConstraint(
            "LENGTH(hashed_password) = 97",
            name="users_hashed_password_length",
        ),
        CheckConstraint(
            "created_at <= CURRENT_TIMESTAMP",
            name="users_created_at_check",
        ),
        CheckConstraint(
            "updated_at IS NULL OR" " updated_at <= CURRENT_TIMESTAMP",
            name="users_updated_at_check",
        ),
    )
