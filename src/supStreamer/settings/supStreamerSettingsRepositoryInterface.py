from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class SupStreamerSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def areCustomSupMessagesEnabled(self) -> bool:
        pass
