from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class FuntoonTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def getToken(
        self,
        twitchChannelId: str
    ) -> str | None:
        pass

    @abstractmethod
    async def requireToken(
        self,
        twitchChannelId: str
    ) -> str:
        pass

    @abstractmethod
    async def setToken(
        self,
        token: str | None,
        twitchChannelId: str
    ):
        pass
