from abc import ABC, abstractmethod

from .mostRecentChat import MostRecentChat
from ..misc.clearable import Clearable


class MostRecentChatsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> MostRecentChat | None:
        pass

    @abstractmethod
    async def set(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ):
        pass
