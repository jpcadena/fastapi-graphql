"""
A module for schemas in the app-schemas package.
"""

from datetime import datetime
from typing import Any, cast
from uuid import uuid4

from pydantic.config import JsonDict

from app.config.config import auth_setting, init_setting
from app.schemas.infrastructure.http_method import HttpMethod
from app.schemas.infrastructure.scope import Scope

public_claims_token_example: JsonDict = {
    "example": {
        "nickname": "username",
        "email": "example@mail.com",
        "preferred_name": "username",
        "updated_at": datetime.now().strftime(init_setting.DATETIME_FORMAT),
    }
}
registered_claims_token_example: JsonDict = {
    "example": {
        "iss": f"{auth_setting.SERVER_URL}",
        "sub": "username:c3ee0ef6-3a18-4251-af6d-138a8c8fec25",
        "aud": f"{auth_setting.SERVER_URL}:80" f"/{auth_setting.TOKEN_URL}",
        "exp": 1672433102,
        "nbf": 1672413301,
        "iat": 1672413302,
        "jti": str(uuid4()),
        "sid": str(uuid4()),
        "scope": f"{Scope.ACCESS_TOKEN}",
        "at_use_nbr": 1,
        "nationalities": ["ECU"],
        "htm": f"{HttpMethod.POST}",
        "htu": f"{auth_setting.AUDIENCE}",
    }
}


def merge_examples(*examples: Any) -> JsonDict:
    """
    Helper function to merge examples
    :param examples:
    :type examples:
    :return:
    :rtype:
    """
    merged_example: JsonDict = {}
    for example in examples:
        merged_example.update(cast(JsonDict, example))
    return {"example": merged_example}


token_payload_example: JsonDict = merge_examples(
    public_claims_token_example["example"],
    registered_claims_token_example["example"],
)
