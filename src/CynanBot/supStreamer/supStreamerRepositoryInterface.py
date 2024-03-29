from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.supStreamer.supStreamerAction import SupStreamerAction


class SupStreamerRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> SupStreamerAction | None:
        pass

    @abstractmethod
    async def update(self, chatterUserId: str, twitchChannelId: str):
        pass
