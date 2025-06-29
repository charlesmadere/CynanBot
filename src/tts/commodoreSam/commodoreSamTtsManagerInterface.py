from abc import ABC

from ..models.ttsProvider import TtsProvider
from ..ttsManagerInterface import TtsManagerInterface


class CommodoreSamTtsManagerInterface(TtsManagerInterface, ABC):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
