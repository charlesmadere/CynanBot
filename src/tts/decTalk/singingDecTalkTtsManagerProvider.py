from .decTalkTtsManagerProvider import DecTalkTtsManagerProvider
from ..models.ttsProvider import TtsProvider


class SingingDecTalkTtsManagerProvider(DecTalkTtsManagerProvider):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.SINGING_DEC_TALK
