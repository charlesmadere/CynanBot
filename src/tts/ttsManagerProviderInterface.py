from abc import ABC, abstractmethod

from .models.ttsProvider import TtsProvider
from .ttsManagerInterface import TtsManagerInterface


class TtsManagerProviderInterface(ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> TtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> TtsManagerInterface | None:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
