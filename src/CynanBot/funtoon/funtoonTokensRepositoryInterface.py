from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class FuntoonTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def getToken(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str | None:
        pass

    @abstractmethod
    async def requireToken(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ) -> str:
        pass

    @abstractmethod
    async def setToken(
        self,
        token: str | None,
        twitchChannel: str,
        twitchChannelId: str
    ):
        pass
