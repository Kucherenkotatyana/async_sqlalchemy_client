from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from dto.user import UserDTO
from models.user import User
from services.interfaces import IUser


class UserService(IUser):

    def __init__(
            self,
            async_session: async_sessionmaker[AsyncSession],
    ) -> None:
        self._model = User
        self._async_session = async_session

    async def add(self, user_dto: UserDTO) -> UserDTO:
        # Creating a separate async session for communication with
        # database. As it was mentioned in the sqlalchemy documentation:
        # session 'represents a “holding zone” for all the objects which
        # we're loading or associating with it during its lifespan'.
        async with self._async_session() as session:

            # Enable UserDTO to validate data before we
            # add it to the database.
            user = self._model(name=user_dto.name)

            # add changes to the Session.
            session.add(user)

            # apply changes to the database.
            await session.commit()

            # Re-load the data from the database in
            # order to get the created object pk.
            await session.refresh(user)

            # Validate data & create a pydantic model instance.
            return UserDTO.model_validate(user)

    async def get(self, pk: int) -> UserDTO:
        async with self._async_session() as session:
            user = await session.get(self._model, pk)
            return UserDTO.model_validate(user)
