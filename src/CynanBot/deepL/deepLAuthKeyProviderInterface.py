from abc import ABC, abstractmethod


class DeepLAuthKeyProviderInterface(ABC):

    @abstractmethod
    async def getDeepLAuthKey(self) -> str | None:
        pass
