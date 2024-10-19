from abc import abstractmethod

from ..misc.clearable import Clearable


class TrollmojiHelperInterface(Clearable):

    @abstractmethod
    async def getEmote(
        self,
        emoteText: str | None,
        twitchEmoteChannelId: str
    ) -> str | None:
        pass

    @abstractmethod
    async def getGottemEmote(self) -> str | None:
        pass

    @abstractmethod
    async def getHypeEmote(self) -> str | None:
        pass
