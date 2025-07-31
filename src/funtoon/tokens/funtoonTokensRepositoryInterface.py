from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class FuntoonTokensRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getToken(
        self,
        twitchChannelId: str,
    ) -> str | None:
        pass

    @abstractmethod
    async def requireToken(
        self,
        twitchChannelId: str,
    ) -> str:
        pass

    @abstractmethod
    async def setToken(
        self,
        token: str | None,
        twitchChannelId: str,
    ):
        pass
