from abc import ABC, abstractmethod

from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class TtsMonsterTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> TtsMonsterTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> TtsMonsterTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
