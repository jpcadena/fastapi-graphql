"""
Package app-models initialization.
"""

from ..db.base_class import Base
from .employer import Employer
from .job import Job

# Export a list of models in the order you want them created.
__all__: list[Base] = [  # type: ignore
    Employer,
    Job,
]
