from abc import abstractmethod

from ..misc.clearable import Clearable
from .mostRecentChat import MostRecentChat


class MostRecentChatsRepositoryInterface(Clearable):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> MostRecentChat | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ):
        pass
