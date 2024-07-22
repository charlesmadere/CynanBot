from abc import ABC, abstractmethod


class StreamElementsUserIdProviderInterface(ABC):

    @abstractmethod
    async def getStreamElementsUserId(self) -> str | None:
        pass
