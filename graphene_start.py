"""
A module for graphene start in the  package.
"""

from typing import Any, Optional, Union

from graphene import Field, Int, Mutation, ObjectType, Schema, String
from graphql import ExecutionResult


class UserType(ObjectType):  # type: ignore
    id: Int = Int()
    name: String = String()
    age: Int = Int()


class CreateUser(Mutation):  # type: ignore
    class Arguments:
        name = String()
        age = Int()

    user: Field = Field(UserType)

    @staticmethod
    def mutate(
        root: Optional[Any], info: Optional[Any], name: str, age: int
    ) -> "CreateUser":
        user_data: dict[str, Union[int, str]] = {
            "id": len(Query.users) + 1,
            "name": name,
            "age": age,
        }
        Query.users.append(user_data)
        create_user: CreateUser = CreateUser(user=UserType(**user_data))
        return create_user


class UpdateUser(Mutation):  # type: ignore
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user: Field = Field(UserType)

    @staticmethod
    def mutate(
        root: Optional[Any],
        info: Optional[Any],
        user_id: int,
        name: Optional[str] = None,
        age: Optional[int] = None,
    ) -> Optional["UpdateUser"]:
        updated_user: Optional[dict[str, int | str]] = next(
            (user for user in Query.users if user["id"] == user_id), None
        )
        if not updated_user:
            return None
        if name is not None:
            updated_user["name"] = name
        if age is not None:
            updated_user["age"] = age
        return UpdateUser(user=updated_user)


class DeleteUser(Mutation):  # type: ignore
    class Arguments:
        user_id = Int(required=True)

    user: Field = Field(UserType)

    @staticmethod
    def mutate(
        root: Optional[Any], info: Optional[Any], user_id: int
    ) -> Optional["DeleteUser"]:
        deleted_user: Optional[dict[str, int | str]] = None
        for idx, user in enumerate(Query.users):
            if user["id"] == user_id:
                deleted_user = user
                del Query.users[idx]
                break
        return DeleteUser(user=deleted_user) if deleted_user else None


class Query(ObjectType):  # type: ignore
    hello: String = String(name=String(default_value="world"))

    @staticmethod
    def resolve_hello(
        root: Optional[Any], info: Optional[Any], name: str
    ) -> str:
        return f"Hello {name}"

    # user: Field = Field(UserType, user_id=Int())
    # users_by_min_age: List = List(UserType, min_age=Int())
    #
    # users: list[dict[str, Union[int, str]]] = [
    #     {"id": 1, "name": "Andy Doe", "age": 33},
    #     {"id": 2, "name": "Andre Doe", "age": 34},
    #     {"id": 3, "name": "Julie Barber", "age": 31},
    #     {"id": 4, "name": "John Doe", "age": 29},
    # ]
    #
    # @staticmethod
    # def resolve_user(
    #     root: Any, info: Any, user_id: int  # root: parent or source
    # ) -> Optional[dict[str, Union[int, str]]]:
    #     matched_users: list[dict[str, int | str]] = [
    #         user for user in Query.users if user["id"] == user_id
    #     ]
    #     return matched_users[0] if matched_users else None
    #
    # @staticmethod
    # def resolve_users_by_min_age(
    #     root: Any, info: Any, min_age: int  # root: parent or source
    # ) -> list[dict[str, Union[int, str]]]:
    #     return [
    #         user
    #         for user in Query.users
    #         if user["age"] >= min_age  # type: ignore
    #     ]


class MyMutations(ObjectType):  # type: ignore
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema: Schema = Schema(query=Query)
# schema: Schema = Schema(query=Query, mutation=MyMutations)

gql: str = """
mutation {
    deleteUser(userId: 1) {
        user {
            id
            name
            age
        }
    }
}
"""

# gql: str = '''
# mutation {
#     updateUser(userId: 1, name: "Updated One", age: 49) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''
# gql: str = '''
# mutation {
#     createUser(name: "Some One", age: 24) {
#         user {
#             id
#             name
#             age
#         }
#     }
# }
# '''
# gql: str = '''
# query {
#     usersByMinAge(minAge: 30) {
#         id
#         name
#         age
#     }
# }
# '''
# gql: str = '''
# query {
#     user(userId: 2) {
#         id
#         name
#         age
#     }
# }
# '''
# gql: str = '''
# {
#     hello(name: "Jay-P")
# }
# '''


if __name__ == "__main__":
    result: ExecutionResult = schema.execute(gql, root_value="some value")
    print(result)
