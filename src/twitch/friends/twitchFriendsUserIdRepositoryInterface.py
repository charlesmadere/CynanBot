from abc import ABC, abstractmethod


class TwitchFriendsUserIdRepositoryInterface(ABC):

    @abstractmethod
    async def getCharlesUserId(self) -> str | None:
        pass
