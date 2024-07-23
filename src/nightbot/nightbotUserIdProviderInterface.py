from abc import ABC, abstractmethod


class NightbotUserIdProviderInterface(ABC):

    @abstractmethod
    async def getNightbotUserId(self) -> str | None:
        pass
