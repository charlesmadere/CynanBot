from abc import ABC, abstractmethod


class TheRunBotUserIdProviderInterface(ABC):

    @abstractmethod
    async def getTheRunBotUserId(self) -> str | None:
        pass
