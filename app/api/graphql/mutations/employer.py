"""
A module for employer in the app.api.graphql.mutations package.
"""

from typing import Optional

from graphene import Boolean, Field, Int, Mutation, String
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo
from pydantic import EmailStr, PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.graphql.types.employer import EmployerType
from app.api.oauth2_validation import admin_user, authenticate_user
from app.config.config import auth_setting
from app.db.session import get_session
from app.exceptions.exceptions import DatabaseException, ServiceException
from app.models.employer import Employer
from app.schemas.external.user import UserAuth


class AddEmployer(Mutation):  # type: ignore
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerType)

    @staticmethod
    @admin_user
    async def mutate(
        root: Optional[Employer],
        info: Optional[GraphQLResolveInfo],
        name: str,
        contact_email: EmailStr,
        industry: str,
    ) -> "AddEmployer":
        if not info:
            raise GraphQLError("No information for authentication")
        user: UserAuth = await authenticate_user(info.context, auth_setting)
        if not user:
            raise ServiceException("User not authenticated")
        employer = Employer(
            name=name, contact_email=contact_email, industry=industry
        )
        async_session: AsyncSession = await get_session()
        async_session.add(employer)
        await async_session.commit()
        return AddEmployer(employer=employer, authenticated=user.email)


class UpdateEmployer(Mutation):  # type: ignore
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerType)

    # temporary
    authenticated = Field(String)

    @staticmethod
    @admin_user
    async def mutate(
        root: Optional[Employer],
        info: Optional[GraphQLResolveInfo],
        _id: PositiveInt,
        name: Optional[str] = None,
        contact_email: Optional[EmailStr] = None,
        industry: Optional[str] = None,
    ) -> "UpdateEmployer":
        async_session: AsyncSession = await get_session()
        employer = await async_session.get(Employer, _id)
        if not employer:
            raise DatabaseException("Employer not found")
        if name is not None:
            employer.name = name
        if contact_email is not None:
            employer.contact_email = contact_email
        if industry is not None:
            employer.industry = industry
        await async_session.commit()
        return UpdateEmployer(employer=employer)


class DeleteEmployer(Mutation):  # type: ignore
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    @admin_user
    async def mutate(
        root: Optional[Employer],
        info: Optional[GraphQLResolveInfo],
        _id: PositiveInt,
    ) -> "DeleteEmployer":
        async_session: AsyncSession = await get_session()
        employer = await async_session.get(Employer, _id)
        if not employer:
            raise DatabaseException("Employer not found")
        await async_session.delete(employer)
        await async_session.commit()
        return DeleteEmployer(success=True)
