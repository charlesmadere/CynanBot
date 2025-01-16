from abc import abstractmethod

from .supStreamerChatter import SupStreamerChatter
from ..misc.clearable import Clearable


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
