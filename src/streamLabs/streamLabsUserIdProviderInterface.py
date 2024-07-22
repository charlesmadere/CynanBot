from abc import ABC, abstractmethod


class StreamLabsUserIdProviderInterface(ABC):

    @abstractmethod
    async def getStreamLabsUserId(self) -> str | None:
        pass
