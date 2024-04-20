import asyncio
import logging

from asyncpg.exceptions import DataError
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncEngine

from database.client import engine
from database.session import get_async_session
from dto.user import UserDTO
from services.user import UserService

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


async def user_service_add(name: str, async_engine: AsyncEngine) -> None:
    async_session = await get_async_session(async_engine)

    user_service = UserService(async_session)
    try:
        result = await user_service.add(UserDTO(name=name))
        logger.debug(f"{result=}")
    except (ValidationError, Exception) as e:
        logger.error(e)


async def user_service_get(pk: int, async_engine: AsyncEngine) -> None:
    async_session = await get_async_session(async_engine)

    user_service = UserService(async_session)
    try:
        result = await user_service.get(pk=pk)
        logger.debug(f"{result=}")
    except (ValidationError, DataError, DBAPIError, Exception) as e:
        logger.error(e)


if __name__ == "__main__":
    # asyncio.run(user_service_get(1, engine))  # noqa
    asyncio.run(user_service_add("Test", engine))
