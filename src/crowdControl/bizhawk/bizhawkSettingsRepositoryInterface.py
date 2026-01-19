from abc import ABC, abstractmethod

from ..actions.crowdControlButton import CrowdControlButton
from ..bizhawk.bizhawkKey import BizhawkKey
from ...misc.clearable import Clearable


class BizhawkSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getButtonKeyBind(
        self,
        button: CrowdControlButton,
    ) -> BizhawkKey | None:
        pass

    @abstractmethod
    async def getGameShuffleKeyBind(self) -> BizhawkKey | None:
        pass

    @abstractmethod
    async def getProcessName(self) -> str:
        pass
