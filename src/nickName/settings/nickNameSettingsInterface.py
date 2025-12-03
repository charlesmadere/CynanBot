from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class NickNameSettingsInterface(Clearable, ABC):

    @abstractmethod
    async def isEnabled(self) -> bool:
        pass
