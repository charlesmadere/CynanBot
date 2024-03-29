from abc import ABC, abstractmethod


class SuperTriviaCooldownHelperInterface(ABC):

    @abstractmethod
    async def getTwitchChannelsInCooldown(self) -> set[str]:
        pass

    @abstractmethod
    def isTwitchChannelInCooldown(self, twitchChannel: str) -> bool:
        pass

    @abstractmethod
    async def update(self, twitchChannel: str):
        pass
