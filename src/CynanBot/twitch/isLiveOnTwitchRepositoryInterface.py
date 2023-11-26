from abc import abstractmethod
from typing import Dict, List

from CynanBot.misc.clearable import Clearable


class IsLiveOnTwitchRepositoryInterface(Clearable):

    @abstractmethod
    async def isLive(self, twitchHandles: List[str]) -> Dict[str, bool]:
        pass
