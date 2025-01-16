from abc import ABC, abstractmethod


class SeryBotUserIdProviderInterface(ABC):

    @abstractmethod
    async def getSeryBotUserId(self) -> str | None:
        pass
