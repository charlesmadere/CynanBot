from abc import ABC, abstractmethod

from .commodoreSamTtsManagerInterface import CommodoreSamTtsManagerInterface
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
