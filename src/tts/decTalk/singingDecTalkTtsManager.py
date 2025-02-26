from .decTalkTtsManager import DecTalkTtsManager
from ..models.ttsProvider import TtsProvider


class SingingDecTalkTtsManager(DecTalkTtsManager):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.SINGING_DEC_TALK
