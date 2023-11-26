from abc import abstractmethod
from typing import Optional

from CynanBot.misc.clearable import Clearable
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat


class MostRecentChatsRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, chatterUserId: str, twitchChannelId: str) -> Optional[MostRecentChat]:
        pass

    @abstractmethod
    async def set(self, chatterUserId: str, twitchChannelId: str):
        pass
