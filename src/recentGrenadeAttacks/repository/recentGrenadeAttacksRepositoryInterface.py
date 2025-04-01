from abc import ABC, abstractmethod

from ..models.recentGrenadeAttackData import RecentGrenadeAttackData
from ...misc.clearable import Clearable


class RecentGrenadeAttacksRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def add(
        self,
        maximumGrenades: int | None,
        attackedUserId: str,
        attackerUserId: str,
        twitchChannelId: str
    ):
        pass

    @abstractmethod
    async def get(
        self,
        attackerUserId: str,
        twitchChannelId: str
    ) -> RecentGrenadeAttackData:
        pass
