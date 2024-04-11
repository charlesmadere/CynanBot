from abc import abstractmethod

from CynanBot.misc.clearable import Clearable
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat


class MostRecentChatsRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, chatterUserId: str, twitchChannelId: str) -> MostRecentChat | None:
        pass

    @abstractmethod
    async def set(self, chatterUserId: str, twitchChannelId: str):
        pass
