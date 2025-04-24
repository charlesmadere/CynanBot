from abc import ABC, abstractmethod

from .ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
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
