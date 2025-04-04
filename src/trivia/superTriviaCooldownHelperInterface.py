from abc import ABC, abstractmethod


class SuperTriviaCooldownHelperInterface(ABC):

    @abstractmethod
    async def getTwitchChannelIdsInCooldown(self) -> frozenset[str]:
        pass

    @abstractmethod
    def isTwitchChannelInCooldown(self, twitchChannelId: str) -> bool:
        pass

    @abstractmethod
    async def update(self, twitchChannelId: str):
        pass
