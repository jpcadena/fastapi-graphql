"""
A module for user in the app.api.graphql.mutations package.
"""

from typing import Any, Optional

from graphene import Field, Int, Mutation, String
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo
from pydantic import EmailStr, PositiveInt
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.graphql.types.application import ApplicationType
from app.api.graphql.types.user import UserType
from app.api.oauth2_validation import admin_user, auth_same_user
from app.config.config import auth_setting
from app.core.security.jwt import build_payload, create_access_token
from app.core.security.password import hash_password, verify_password
from app.db.session import get_session
from app.exceptions.exceptions import NotFoundException
from app.models.application import Application
from app.models.employer import Employer
from app.models.job import Job
from app.models.user import User
from app.schemas.external.token import TokenPayload


class LoginUser(Mutation):  # type: ignore
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    async def mutate(
        root: Optional[Employer],
        info: Optional[GraphQLResolveInfo],
        email: EmailStr,
        password: str,
    ) -> "LoginUser":
        stmt: Select[Any]
        async_session: AsyncSession = await get_session()
        stmt = select(User).where(User.email == email)
        try:
            user: User | None = (await async_session.scalars(stmt)).first()
        except SQLAlchemyError as sa_exc:
            raise sa_exc
        if not user:
            raise NotFoundException("User could not be found")
        if not verify_password(user.hashed_password, password):
            raise GraphQLError("Invalid email or password")
        access_payload: TokenPayload = build_payload(user, auth_setting)
        access_token: str = create_access_token(access_payload, auth_setting)
        return LoginUser(token=access_token)


class AddUser(Mutation):  # type: ignore
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserType)

    @staticmethod
    @admin_user
    async def mutate(
        root: User | None,
        info: GraphQLResolveInfo | None,
        username: str,
        email: EmailStr,
        password: str,
        role: str,
    ) -> "AddUser":
        async_session: AsyncSession = await get_session()
        stmt = select(User).where(User.email == email)
        try:
            user_obj: User | None = (await async_session.scalars(stmt)).first()
        except SQLAlchemyError as sa_exc:
            raise sa_exc
        if user_obj:
            raise NotFoundException("User already exists with that email")
        hashed_password: str = hash_password(password)
        user: User = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role,
        )
        async_session.add(user)
        await async_session.commit()
        return AddUser(user=user)


class ApplyToJob(Mutation):  # type: ignore
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    application = Field(lambda: ApplicationType)

    @staticmethod
    @auth_same_user
    async def mutate(
        root: Job | None,
        info: GraphQLResolveInfo | None,
        user_id: PositiveInt,
        job_id: PositiveInt,
    ) -> "ApplyToJob":
        async_session: AsyncSession = await get_session()
        stmt = select(Application).where(
            Application.user_id == user_id and Application.job_id == job_id
        )
        try:
            application: Application | None = (
                await async_session.scalars(stmt)
            ).first()
        except SQLAlchemyError as sa_exc:
            raise sa_exc
        async_session.add(application)
        await async_session.commit()
        return ApplyToJob(application=application)
