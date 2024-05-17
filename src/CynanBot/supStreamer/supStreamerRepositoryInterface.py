from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.supStreamer.supStreamerChatter import SupStreamerChatter


class SupStreamerRepositoryInterface(Clearable):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> SupStreamerChatter | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass
