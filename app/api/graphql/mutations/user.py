"""
A module for user in the app.api.graphql.mutations package.
"""

from typing import Any, Optional

from graphene import Mutation, String
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo
from pydantic import EmailStr
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.config import auth_setting
from app.core.security.jwt import build_payload, create_access_token
from app.core.security.password import verify_password
from app.db.session import get_session
from app.exceptions.exceptions import NotFoundException
from app.models.employer import Employer
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
