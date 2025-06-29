from abc import ABC

from ..models.ttsProvider import TtsProvider
from ..ttsManagerInterface import TtsManagerInterface


class MicrosoftSamTtsManagerInterface(TtsManagerInterface, ABC):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
