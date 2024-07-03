from abc import ABC, abstractmethod


class TwitchAnonymousUserIdProviderInterface(ABC):

    @abstractmethod
    async def getTwitchAnonymousUserId(self) -> str:
        pass
