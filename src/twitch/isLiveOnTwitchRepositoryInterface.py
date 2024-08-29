from abc import abstractmethod

from frozendict import frozendict

from ..misc.clearable import Clearable


class IsLiveOnTwitchRepositoryInterface(Clearable):

    @abstractmethod
    async def areLive(self, twitchChannelIds: set[str]) -> frozendict[str, bool]:
        pass

    @abstractmethod
    async def isLive(self, twitchChannelId: str) -> bool:
        pass
