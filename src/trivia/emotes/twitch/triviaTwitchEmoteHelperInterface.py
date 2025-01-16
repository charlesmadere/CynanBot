from abc import ABC, abstractmethod


class TriviaTwitchEmoteHelperInterface(ABC):

    @abstractmethod
    async def getCelebratoryEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getOutOfTimeEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getWrongAnswerEmote(self) -> str | None:
        pass
