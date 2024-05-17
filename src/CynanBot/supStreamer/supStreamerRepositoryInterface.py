from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.supStreamer.supStreamerChatter import SupStreamerChatter


class SupStreamerRepositoryInterface(Clearable):

    @abstractmethod
    async def getChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> SupStreamerChatter:
        pass

    @abstractmethod
    async def updateChatter(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass
