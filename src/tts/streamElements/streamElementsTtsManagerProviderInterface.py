from abc import ABC, abstractmethod

from .streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class StreamElementsTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> StreamElementsTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> StreamElementsTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS
