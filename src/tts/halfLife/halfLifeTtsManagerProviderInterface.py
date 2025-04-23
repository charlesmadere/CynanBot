from abc import ABC, abstractmethod

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class HalfLifeTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> HalfLifeTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> HalfLifeTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
