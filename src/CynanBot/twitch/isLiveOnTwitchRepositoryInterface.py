from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class IsLiveOnTwitchRepositoryInterface(Clearable):

    @abstractmethod
    async def areLive(self, twitchChannelIds: set[str]) -> dict[str, bool]:
        pass

    @abstractmethod
    async def isLive(self, twitchChannelId: str) -> bool:
        pass
