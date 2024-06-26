"""
A module for region in the app-models package.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import UUID4
from sqlalchemy import CheckConstraint, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.config import sql_database_setting
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.locality import Locality


class Region(Base):  # type: ignore
    """
    Region model class representing the "region" table
    """

    __tablename__ = "region"
    id: Mapped[UUID4] = mapped_column(
        UUID(as_uuid=True),
        index=True,
        nullable=False,
        primary_key=True,
        unique=True,
        comment="ID of the region",
    )
    code: Mapped[str] = mapped_column(
        String(2),
        index=True,
        nullable=False,
        unique=True,
        comment="Code of the region",
    )
    region: Mapped[str] = mapped_column(
        String(35),
        nullable=False,
        unique=True,
        comment="State, province, prefecture, or region component",
    )
    capital: Mapped[str] = mapped_column(
        String(30), nullable=False, unique=True, comment="Capital of province"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        default=datetime.now(),
        nullable=False,
        server_default=text("now()"),
        comment="Time the region was created",
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(
            timezone=True, precision=sql_database_setting.TIMESTAMP_PRECISION
        ),
        nullable=True,
        comment="Time the region was updated",
    )

    localities: Mapped[list["Locality"]] = relationship(
        "Locality", back_populates="region"
    )

    __table_args__ = (
        CheckConstraint("char_length(region) >= 4"),
        CheckConstraint("char_length(capital) >= 4"),
        CheckConstraint(
            sql_database_setting.DB_REGION_CODE_CONSTRAINT,
            name="region_code_format",
        ),
    )
