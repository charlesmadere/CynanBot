from abc import ABC, abstractmethod

from .models.ttsProvider import TtsProvider
from .ttsManagerInterface import TtsManagerInterface


class TtsManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> TtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> TtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
