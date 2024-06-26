"""
A module for address in the app-models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import CheckConstraint, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import init_setting, sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User


class Address(Base):  # type: ignore
    """
    UserAddress model class representing the "user_address" table
    """

    __tablename__ = "users_address"

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        primary_key=True,
        unique=True,
        server_default=text("(gen_random_uuid())"),
        comment="ID of the User Address",
    )
    street_address: Mapped[str] = mapped_column(
        String(150), nullable=True, comment="Street address of the User"
    )
    locality: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="Locality (City) for address of the User",
    )
    region: Mapped[str] = mapped_column(
        String(100),
        default=init_setting.DEFAULT_REGION,
        nullable=True,
        comment="Region (State/Province) for address of the User",
    )
    country: Mapped[str] = mapped_column(
        String(100), nullable=True, comment="Country for address of the User"
    )
    postal_code: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        comment="Postal code should be a 6-digit number.",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the User Address was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        nullable=True,
        comment="Time the User Address was updated",
    )

    users: Mapped[list["User"]] = relationship("User", back_populates="address")

    __table_args__ = (
        CheckConstraint(
            "char_length(street_address) >= 3",
            name="address_street_address_length",
        ),
        CheckConstraint(
            "char_length(locality) >= 3", name="address_locality_length"
        ),
        CheckConstraint(
            "char_length(region) >= 4", name="address_region_length"
        ),
        CheckConstraint(
            "char_length(country) >= 4", name="address_country_length"
        ),
        CheckConstraint(
            "LENGTH(postal_code) = 6", name="address_postal_code_length"
        ),
        CheckConstraint(
            f"postal_code ~ '"
            f"{sql_database_setting.DB_POSTAL_CODE_CONSTRAINT}'",
            name="address_postal_code_format",
        ),
    )
