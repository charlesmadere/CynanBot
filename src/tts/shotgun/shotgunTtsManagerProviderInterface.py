from abc import ABC, abstractmethod

from .shotgunTtsManagerInterface import ShotgunTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class ShotgunTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> ShotgunTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> ShotgunTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.SHOTGUN_TTS
