"""
A module for utils in the app.utils package.
"""

import logging
import math
from typing import Any

import phonenumbers
import pycountry
from fastapi import Depends
from pydantic import EmailStr, PositiveInt
from pydantic_extra_types.phone_numbers import PhoneNumber

from app.config.config import get_init_settings
from app.config.init_settings import InitSettings
from app.utils.file_utils.json_utils import read_json_file, write_json_file
from app.utils.file_utils.openapi_utils import modify_json_data

logger: logging.Logger = logging.getLogger(__name__)


async def update_json(
    init_setting: InitSettings = Depends(get_init_settings),
) -> None:
    """
    Update JSON file for client
    :param init_setting: Dependency method for cached setting object
    :type init_setting: InitSettings
    :return: None
    :rtype: NoneType
    """
    data: dict[str, Any] = await read_json_file(init_setting)
    data = modify_json_data(data)
    await write_json_file(data, init_setting)
    logger.info("Updated OpenAPI JSON file")


def hide_email(email: EmailStr) -> str:
    """
    Hide email using **** for some characters
    :param email: Email address to hide some values
    :type email: EmailStr
    :return: Email address with some **** for its value
    :rtype: str
    """
    email_title, email_domain = email.split("@")
    title_count: PositiveInt = max(math.ceil(len(email_title) / 2), 1)
    domain_sections = email_domain.split(".")
    domain_first_section = domain_sections[0]
    domain_count: PositiveInt = max(math.ceil(len(domain_first_section) / 2), 1)
    replaced_title: str = email_title.replace(
        email_title[title_count * -1 :], "*" * title_count
    )
    replaced_domain_first: str = domain_first_section.replace(
        domain_first_section[domain_count * -1 :], "*" * domain_count
    )
    replaced_domain: str = f"{replaced_domain_first}." + ".".join(
        domain_sections[1:]
    )
    hidden_email: str = f"{replaced_title}@{replaced_domain}"
    return hidden_email


def get_nationality_code(country_name: str) -> str:
    """
    Get the nationality code given a country name
    :param country_name: The name of the country
    :type country_name: str
    :return: The nationality in ICAO 3-letter code [ICAO-Doc9303]
    :rtype: str
    """
    try:
        if country := pycountry.countries.get(name=country_name):
            return str(country.alpha_3)
    except LookupError:
        pass
    return ""


def validate_phone_number(phone_number: PhoneNumber) -> PhoneNumber:
    """
    Validate the phone number format
    :param phone_number: The phone number to validate
    :type phone_number: str
    :return: The validated phone number
    :rtype: str
    """
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
    except phonenumbers.phonenumberutil.NumberParseException as exc:
        raise ValueError from exc
    if not phonenumbers.is_valid_number(parsed_number):
        raise ValueError("Invalid phone number")
    return phone_number
