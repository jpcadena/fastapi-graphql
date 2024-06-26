"""
A module for common attributes between User and Token in the app-schemas
package.
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, PastDate
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.api.graphql.schemas.external.address import Address
from app.api.graphql.schemas.infrastructure.gender import Gender
from app.config.config import init_setting


class EditableData(BaseModel):
    """
    Editable fields for User and Token classes based on Pydantic
     Base Model.
    """

    phone_number: Optional[PhoneNumber] = Field(
        default=None,
        title="Telephone",
        description="Preferred telephone number of the User",
        validate_default=True,
    )
    address: Address = Field(
        default=...,
        title="Address",
        description="Preferred postal address of the User",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "phone_number": "+5939987654321",
                "address": Address(
                    street_address="Blvd 9 de Octubre",
                    locality="Guayaquil",
                    region=init_setting.DEFAULT_REGION,
                    country=init_setting.DEFAULT_COUNTRY,
                    postal_code="090312",
                ).model_dump(),
            }
        },
    )


class CommonUserToken(EditableData):
    """
    Common fields for User and Token classes based on EditableData.
    """

    given_name: str = Field(
        ...,
        title="First name",
        description="Given name(s) or first name(s) of the User",
        min_length=1,
        max_length=50,
    )
    family_name: str = Field(
        ...,
        title="Last name",
        description="Surname(s) or last name(s) of the User",
        min_length=1,
        max_length=50,
    )
    middle_name: Optional[str] = Field(
        ...,
        title="Middle name",
        description="Middle name(s) of the User",
        max_length=50,
    )
    gender: Optional[Gender] = Field(
        default=Gender.MALE, title="Gender", description="Gender of the User"
    )
    birthdate: Optional[PastDate] = Field(
        default=None, title="Birthdate", description="Birthday of the User"
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        title="Updated at",
        description="Time the User information was last updated",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "given_name": "Some",
                "family_name": "Example",
                "middle_name": "One",
                "gender": Gender.MALE,
                "birthdate": date(2002, 1, 1).strftime("%Y-%m-%d"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "phone_number": "+5939987654321",
                "address": Address(
                    street_address="Blvd 9 de Octubre",
                    locality="Guayaquil",
                    region=init_setting.DEFAULT_REGION,
                    country=init_setting.DEFAULT_COUNTRY,
                    postal_code="090312",
                ).model_dump(),
            }
        },
    )
