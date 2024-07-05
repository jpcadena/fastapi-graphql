"""
Package app-models initialization.
"""

from ..db.base_class import Base
from .application import Application
from .employer import Employer
from .job import Job
from .user import User

# Export a list of models in the order you want them created.
__all__: list[Base] = [  # type: ignore
    Employer,
    Job,
    User,
    Application,
]
