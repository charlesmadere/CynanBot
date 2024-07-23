from abc import ABC, abstractmethod


class CynanBotUserIdsProviderInterface(ABC):

    @abstractmethod
    async def getCynanBotUserId(self) -> str | None:
        pass

    @abstractmethod
    async def getCynanBotTtsUserId(self) -> str | None:
        pass
