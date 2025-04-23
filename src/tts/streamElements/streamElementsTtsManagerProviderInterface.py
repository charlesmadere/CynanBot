from abc import ABC, abstractmethod

from .streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class StreamElementsTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> StreamElementsTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> StreamElementsTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
