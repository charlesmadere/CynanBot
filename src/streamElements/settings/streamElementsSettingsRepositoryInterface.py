from abc import ABC, abstractmethod

from ..models.streamElementsVoice import StreamElementsVoice
from ...misc.clearable import Clearable


class StreamElementsSettingsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getDefaultVoice(self) -> StreamElementsVoice:
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
