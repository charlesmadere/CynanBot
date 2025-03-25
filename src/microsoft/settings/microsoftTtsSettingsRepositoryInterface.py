from abc import ABC, abstractmethod

from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ...misc.clearable import Clearable


class MicrosoftTtsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getDefaultVoice(self) -> MicrosoftTtsVoice:
        pass

    @abstractmethod
    async def getFileExtension(self) -> str:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def useDonationPrefix(self) -> bool:
        pass
