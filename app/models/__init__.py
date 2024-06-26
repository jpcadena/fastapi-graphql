"""
Package app-models initialization.
"""

from app.models.address import Address
from app.models.locality import Locality
from app.models.region import Region
from app.models.user import User

from ..db.base_class import Base

# Export a list of models in the order you want them created.
__all__: list[Base] = [Address, User, Region, Locality]  # type: ignore
