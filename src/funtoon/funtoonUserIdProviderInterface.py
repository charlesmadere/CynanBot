from abc import ABC, abstractmethod


class FuntoonUserIdProviderInterface(ABC):

    @abstractmethod
    async def getFuntoonUserId(self) -> str | None:
        pass
