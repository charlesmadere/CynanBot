from abc import ABC, abstractmethod


class RecentGrenadeAttacksHelperInterface(ABC):

    @abstractmethod
    async def canThrowGrenade(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> bool:
        pass

    @abstractmethod
    async def fetchAvailableGrenades(
        self,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        pass

    @abstractmethod
    async def throwGrenade(
        self,
        attackedUserId: str,
        attackerUserId: str,
        twitchChannel: str,
        twitchChannelId: str
    ) -> int | None:
        pass
