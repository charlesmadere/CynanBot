from abc import abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice
from ...misc.clearable import Clearable


class StreamElementsSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getDefaultVoice(self) -> StreamElementsVoice:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass
