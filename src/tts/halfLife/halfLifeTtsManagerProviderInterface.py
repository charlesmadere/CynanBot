from abc import ABC, abstractmethod

from .halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class HalfLifeTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True,
    ) -> HalfLifeTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> HalfLifeTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.HALF_LIFE
