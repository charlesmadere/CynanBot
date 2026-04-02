from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class CutenessSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
