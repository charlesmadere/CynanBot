from abc import abstractmethod

from CynanBot.misc.clearable import Clearable


class IsLiveOnTwitchRepositoryInterface(Clearable):

    @abstractmethod
    async def isLive(self, twitchHandles: list[str]) -> dict[str, bool]:
        pass
