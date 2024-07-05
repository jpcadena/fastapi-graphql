"""
A module for user in the app.api.graphql.mutations package.
"""

from random import choices
from string import ascii_lowercase
from typing import Any, Optional

from graphene import Mutation, String
from graphql import GraphQLError
from graphql.type.definition import GraphQLResolveInfo
from pydantic import EmailStr
from sqlalchemy import Select, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.exceptions.exceptions import NotFoundException
from app.models.employer import Employer
from app.models.user import User


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
            db_obj: User | None = (await async_session.scalars(stmt)).first()
        except SQLAlchemyError as sa_exc:
            raise sa_exc
        if not db_obj:
            raise NotFoundException("User could not be found")
        if db_obj.password != password:
            raise GraphQLError("Invalid email or password")
        token: str = "".join(choices(ascii_lowercase, k=10))
        return LoginUser(token=token)
