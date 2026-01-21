"""
Import all ORM models so that metadata can be accessed by Alembic or during startup.
"""

from .customer import Customer  # noqa: F401
from .support_staff import SupportStaff  # noqa: F401
from .product import Product  # noqa: F401
from .order import Order  # noqa: F401
from .message import Message  # noqa: F401
from .user import User  # noqa: F401

# AuditLog is not yet implemented in this simplified example.  In a full
# implementation this would import the AuditLog model for change tracking.

