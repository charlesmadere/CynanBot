from abc import abstractmethod
from typing import List, Optional

from CynanBot.misc.clearable import Clearable
from CynanBot.twitch.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.twitchTokensRepositoryListener import \
    TwitchTokensRepositoryListener


class TwitchTokensRepositoryInterface(Clearable):

    @abstractmethod
    async def addUser(self, code: str, twitchChannel: str):
        pass

    @abstractmethod
    async def getAccessToken(self, twitchChannel: str) -> Optional[str]:
        pass

    @abstractmethod
    async def getExpiringTwitchChannels(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    async def getRefreshToken(self, twitchChannel: str) -> Optional[str]:
        pass

    @abstractmethod
    async def hasAccessToken(self, twitchChannel: str) -> bool:
        pass

    @abstractmethod
    async def removeUser(self, twitchChannel: str):
        pass

    @abstractmethod
    async def requireAccessToken(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def requireRefreshToken(self, twitchChannel: str) -> str:
        pass

    @abstractmethod
    async def requireTokensDetails(self, twitchChannel: str) -> TwitchTokensDetails:
        pass

    @abstractmethod
    def setListener(self, listener: Optional[TwitchTokensRepositoryListener]):
        pass

    @abstractmethod
    async def validateAndRefreshAccessToken(self, twitchChannel: str):
        pass
