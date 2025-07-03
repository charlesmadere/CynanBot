from .decTalkTtsManager import DecTalkTtsManager
from ..models.ttsProvider import TtsProvider


class UnrestrictedDecTalkTtsManager(DecTalkTtsManager):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.UNRESTRICTED_DEC_TALK
