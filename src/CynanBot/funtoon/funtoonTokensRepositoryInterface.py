from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable


class FuntoonTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def getToken(self, twitchChannel: str) -> Optional[str]:
        pass

    @abstractmethod
    async def requireToken(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def setToken(self, token: Optional[str], twitchChannel: str):
        pass
