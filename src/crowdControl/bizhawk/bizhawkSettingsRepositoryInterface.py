from abc import abstractmethod

from ..actions.crowdControlButton import CrowdControlButton
from ..bizhawk.bizhawkKey import BizhawkKey
from ...misc.clearable import Clearable


class BizhawkSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getButtonKeyBind(
        self,
        button: CrowdControlButton
    ) -> BizhawkKey | None:
        pass

    @abstractmethod
    async def getGameShuffleKeyBind(self) -> BizhawkKey | None:
        pass
