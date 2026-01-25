from abc import ABC, abstractmethod


class TwitchCredentialsProviderInterface(ABC):

    @abstractmethod
    async def getTwitchClientId(self) -> str:
        pass

    @abstractmethod
    async def getTwitchClientSecret(self) -> str:
        pass
