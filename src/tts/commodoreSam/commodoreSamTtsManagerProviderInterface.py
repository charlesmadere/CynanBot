from abc import ABC, abstractmethod

from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
from ..models.ttsProvider import TtsProvider
from ..ttsManagerProviderInterface import TtsManagerProviderInterface


class CommodoreSamTtsManagerProviderInterface(TtsManagerProviderInterface, ABC):

    @abstractmethod
    def constructNewInstance(
        self,
        useSharedSoundPlayerManager: bool = True
    ) -> CommodoreSamTtsManagerInterface | None:
        pass

    @abstractmethod
    def getSharedInstance(self) -> CommodoreSamTtsManagerInterface | None:
        pass

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
