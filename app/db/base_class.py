"""
This script defines the base class for SQLAlchemy models
"""

from typing import Type

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

Base: Type[DeclarativeMeta] = declarative_base()
