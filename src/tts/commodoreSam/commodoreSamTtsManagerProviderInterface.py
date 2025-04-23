from abc import ABC, abstractmethod

from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class CommodoreSamTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> CommodoreSamTtsManagerInterface:
        pass

    @abstractmethod
    def getSharedInstance(self) -> CommodoreSamTtsManagerInterface:
        pass

    @property
    @abstractmethod
    def ttsProvider(self) -> TtsProvider:
        pass
