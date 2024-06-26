"""
A module for locality in the app-models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import CheckConstraint, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.region import Region


class Locality(Base):  # type: ignore
    """
    Locality model class representing the "locality" table
    """

    __tablename__ = "locality"

    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        primary_key=True,
        unique=True,
        comment="ID of the Locality",
    )
    locality: Mapped[str] = mapped_column(
        String(4),
        nullable=False,
        unique=True,
        comment="City or locality component",
    )
    region_code: Mapped[str] = mapped_column(
        String(2),
        ForeignKey(
            "region.code",
            name="region_code_fkey",
        ),
        nullable=False,
        comment="Code of the region",
        name="region_code_fkey",
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the locality was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        nullable=True,
        comment="Time the locality was updated",
    )
    region: Mapped[list["Region"]] = relationship(
        "Region", back_populates="localities"
    )

    __table_args__ = (CheckConstraint("char_length(locality) >= 4"),)
