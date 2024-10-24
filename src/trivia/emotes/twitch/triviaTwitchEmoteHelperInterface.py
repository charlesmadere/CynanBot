from abc import abstractmethod

from ....misc.clearable import Clearable


class TriviaTwitchEmoteHelperInterface(Clearable):

    @abstractmethod
    async def getCelebratoryEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getOutOfTimeEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getWrongAnswerEmote(self) -> str | None:
        pass
