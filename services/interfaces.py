from abc import ABC, abstractmethod

from dto.user import UserDTO


class IUser(ABC):

    @abstractmethod
    async def add(self, user_dto: UserDTO) -> UserDTO:
        pass

    @abstractmethod
    async def get(self, pk: int) -> UserDTO:
        pass
