from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """
    Inherited from AsyncAttrs class, since it provides
    an awaitable accessor for all attributes.
    """
