from abc import abstractmethod

from ....misc.clearable import Clearable


class TriviaTwitchEmoteHelperInterface(Clearable):

    @abstractmethod
    async def getCelebratoryEmote(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def getOutOfTimeEmote(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def getWrongAnswerEmote(self, twitchChannelId: str) -> str | None:
        pass
