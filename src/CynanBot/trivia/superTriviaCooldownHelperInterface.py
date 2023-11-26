from abc import ABC, abstractmethod
from typing import Set


class SuperTriviaCooldownHelperInterface(ABC):

    @abstractmethod
    async def getTwitchChannelsInCooldown(self) -> Set[str]:
        pass

    @abstractmethod
    def isTwitchChannelInCooldown(self, twitchChannel: str) -> bool:
        pass

    @abstractmethod
    async def update(self, twitchChannel: str):
        pass
