from abc import abstractmethod

from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc.clearable import Clearable


class MicrosoftSamSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def getDefaultVoice(self) -> MicrosoftSamVoice:
        pass