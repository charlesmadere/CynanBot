from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class RecentGrenadeAttacksSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getGrenadeCooldownSeconds(self) -> int:
        pass
