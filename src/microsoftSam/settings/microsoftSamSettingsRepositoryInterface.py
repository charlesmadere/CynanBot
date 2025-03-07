from abc import ABC, abstractmethod

from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc.clearable import Clearable


class MicrosoftSamSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getDefaultVoice(self) -> MicrosoftSamVoice:
        pass

    @abstractmethod
    async def getFileExtension(self) -> str:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass
