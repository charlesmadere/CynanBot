from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...misc.clearable import Clearable


class TwitchModeratorHelperInterface(Clearable, ABC):

    class AbsRequest(ABC):

        @abstractmethod
        def getChatterUserId(self) -> str:
            pass

        @abstractmethod
        def getTwitchChannelId(self) -> str:
            pass

    @dataclass(frozen = True, slots = True)
    class Request(AbsRequest):
        chatterUserId: str
        twitchChannelId: str

        def getChatterUserId(self) -> str:
            return self.chatterUserId

        def getTwitchChannelId(self) -> str:
            return self.twitchChannelId

    @dataclass(frozen = True, slots = True)
    class RequestWithAccessToken(AbsRequest):
        chatterUserId: str
        twitchAccessToken: str
        twitchChannelId: str

        def getChatterUserId(self) -> str:
            return self.chatterUserId

        def getTwitchChannelId(self) -> str:
            return self.twitchChannelId

    @abstractmethod
    async def isModerator(self, request: Request) -> bool:
        pass
