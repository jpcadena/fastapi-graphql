"""
A module for employer in the app.api.graphql.mutations package.
"""

from typing import Any, Optional

from graphene import Field, Int, Mutation, String
from pydantic import EmailStr, PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.graphql.schemas.external.employer import Employer as EmployerObject
from app.db.session import get_session
from app.models.employer import Employer


class AddEmployer(Mutation):  # type: ignore
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    @staticmethod
    async def mutate(
        root: Optional[Any],
        info: Optional[Any],
        name: str,
        contact_email: EmailStr,
        industry: str,
    ) -> "AddEmployer":
        employer = Employer(
            name=name, contact_email=contact_email, industry=industry
        )
        async_session: AsyncSession = await get_session()
        async_session.add(employer)
        await async_session.commit()
        return AddEmployer(employer=employer)


class UpdateEmployer(Mutation):  # type: ignore
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    async def mutate(
        root: Optional[Any],
        info: Optional[Any],
        _id: PositiveInt,
        name: Optional[str] = None,
        contact_email: Optional[EmailStr] = None,
        industry: Optional[str] = None,
    ) -> "UpdateEmployer":
        async_session: AsyncSession = await get_session()
        employer = await async_session.get(Employer, _id)
        if not employer:
            raise Exception("Employer not found")
        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry
        await async_session.commit()
        return UpdateEmployer(employer=employer)
