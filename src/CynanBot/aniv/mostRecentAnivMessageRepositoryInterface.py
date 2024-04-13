from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class MostRecentAnivMessageRepositoryInterface(Clearable):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, message: str | None, twitchChannelId: str):
        pass
