"""
A module for address in the app-schemas package.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.config.config import init_setting, sql_database_setting


class AddressID(BaseModel):
    """
    Schema for representing an Address's ID.
    """

    id: UUID4 = Field(
        default_factory=UUID4, title="ID", description="ID of the Address"
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"id": str(uuid4())}}
    )


class AddressUpdatedAt(BaseModel):
    """
    Schema for representing the update timestamp of an Address.
    """

    updated_at: Optional[datetime] = Field(
        default=None,
        title="Updated at",
        description="Time the Address was updated",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        },
    )


class AddressUpdate(BaseModel):
    """
    Schema for the Address of a User.
    """

    street_address: str = Field(
        ...,
        title="Street Address",
        description="Full street address component, which may include house"
        " number, street name, Post Office Box, and multi-line"
        " extended street address information. This field ma"
        "y contain multiple lines, separated by newlines.",
        min_length=3,
    )
    locality: str = Field(
        ...,
        title="Locality (City)",
        description="City or locality component.",
        min_length=3,
        max_length=85,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "street_address": "Blvd 9 de Octubre",
                "locality": "Guayaquil",
            }
        },
    )


class AddressResponse(AddressUpdate):
    """
    Schema for representing the Address of a User.
    """

    region: str = Field(
        default=init_setting.DEFAULT_REGION,
        title="Region (State/Province)",
        description="State, province, prefecture, or region component.",
        min_length=4,
        max_length=35,
    )
    country: str = Field(
        default=init_setting.DEFAULT_COUNTRY,
        title="Country",
        description="Country name component.",
        min_length=4,
        max_length=60,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "street_address": "Blvd 9 de Octubre",
                "locality": "Guayaquil",
                "region": init_setting.DEFAULT_REGION,
                "country": init_setting.DEFAULT_COUNTRY,
            }
        },
    )


class Address(AddressResponse):
    """
    Schema for representing the Address for JWT.
    """

    postal_code: Optional[str] = Field(
        None,
        title="Postal Code",
        min_length=6,
        max_length=6,
        pattern=sql_database_setting.DB_POSTAL_CODE_CONSTRAINT,
        description="Postal code should be a 6-digit number.",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "street_address": "Blvd 9 de Octubre",
                "locality": "Guayaquil",
                "region": init_setting.DEFAULT_REGION,
                "country": init_setting.DEFAULT_COUNTRY,
                "postal_code": "090312",
            }
        },
    )


class UserAddressInDB(AddressID, Address, AddressUpdatedAt):
    """
    Schema for updating the Address of a User.
    """

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": str(uuid4()),
                "street_address": "Blvd 9 de Octubre",
                "locality": "Guayaquil",
                "region": init_setting.DEFAULT_REGION,
                "country": init_setting.DEFAULT_COUNTRY,
                "postal_code": "090312",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
        },
    )

    created_at: datetime = Field(
        default_factory=datetime.now,
        title="Created at",
        description="Time the User was created",
    )
