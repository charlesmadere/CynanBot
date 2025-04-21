from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TtsChatterSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def useMessageQueueing(self) -> bool:
        pass
