from abc import ABC, abstractmethod


class TwitchTimeoutHelperInterface(ABC):

    @abstractmethod
    async def timeout(
        self,
        broadcasterUserId: str,
        twitchAccessToken: str,
        userIdToTimeout: str
    ) -> bool:
        pass
