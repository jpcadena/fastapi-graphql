"""
A module for user in the app models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4, EmailStr, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    Enum,
    ForeignKey,
    String,
    text,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.graphql.schemas.infrastructure.gender import Gender
from app.config.config import sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.address import Address


class User(Base):  # type: ignore
    """
    User model class representing the "users" table
    """

    __tablename__ = "users"

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        primary_key=True,
        unique=True,
        server_default=text("(gen_random_uuid())"),
        comment="ID of the User",
    )
    username: Mapped[str] = mapped_column(
        String(15),
        index=True,
        unique=True,
        nullable=False,
        comment="Username to identify the user",
    )
    email: Mapped[EmailStr] = mapped_column(
        String(320),
        index=True,
        unique=True,
        nullable=False,
        comment="Preferred e-mail address of the User",
    )
    first_name: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="First name(s) of the User"
    )
    middle_name: Mapped[str] = mapped_column(
        String(50), nullable=True, comment="Middle name(s) of the User"
    )
    last_name: Mapped[str] = mapped_column(
        String(100), nullable=False, comment="Last name(s) of the User"
    )
    password: Mapped[str] = mapped_column(
        String(60), nullable=False, comment="Hashed password of the User"
    )
    gender: Mapped[Gender] = mapped_column(
        Enum(Gender), nullable=True, comment="Gender of the User"
    )
    birthdate: Mapped[PastDate] = mapped_column(
        Date, nullable=True, comment="Birthday of the User"
    )
    phone_number: Mapped[PhoneNumber] = mapped_column(
        String(20),
        nullable=True,
        comment="Preferred telephone number of the User",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean(),
        default=True,
        nullable=False,
        server_default=text("true"),
        comment="True if the user is active; otherwise false",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="True if the user is super user; otherwise false",
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
        comment="Time the User was updated",
    )
    address_id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users_address.id",
            name="users_address_id_fkey",
        ),
        nullable=False,
        comment="ID of the User's address",
    )
    address: Mapped["Address"] = relationship(
        "Address", back_populates="users", lazy="joined"
    )

    __table_args__ = (
        CheckConstraint(
            "char_length(username) >= 4", name="users_username_length"
        ),
        CheckConstraint("char_length(email) >= 3", name="users_email_length"),
        CheckConstraint(
            sql_database_setting.DB_EMAIL_CONSTRAINT, name="users_email_format"
        ),
        CheckConstraint(
            "char_length(first_name) >= 1", name="users_first_name_length"
        ),
        CheckConstraint(
            "char_length(last_name) >= 1", name="users_last_name_length"
        ),
        CheckConstraint("LENGTH(password) = 60", name="users_password_length"),
        CheckConstraint(
            sql_database_setting.DB_PHONE_NUMBER_CONSTRAINT,
            name="users_phone_number_format",
        ),
    )
