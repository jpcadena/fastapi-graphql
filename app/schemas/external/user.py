"""
A module for user in the app.schemas.external package.
"""

from pydantic import BaseModel, ConfigDict, EmailStr, Field, PositiveInt

from app.schemas.schemas import user_base_auth_example


class UserAuth(BaseModel):
    """
    Schema for representing the basic authentication attributes of a
     User.
    """

    model_config = ConfigDict(
        json_schema_extra=user_base_auth_example,
    )

    id: PositiveInt = Field(..., title="ID", description="ID of the User")
    username: str = Field(
        ...,
        title="Username",
        description="Username to identify the user",
        min_length=4,
        max_length=15,
    )
    email: EmailStr = Field(
        ..., title="Email", description="Preferred e-mail address of the User"
    )
