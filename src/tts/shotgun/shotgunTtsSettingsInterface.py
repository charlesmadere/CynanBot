from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class ShotgunTtsSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
