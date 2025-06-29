from abc import ABC, abstractmethod

from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class TtsMonsterTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> TtsMonsterTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> TtsMonsterTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.TTS_MONSTER
