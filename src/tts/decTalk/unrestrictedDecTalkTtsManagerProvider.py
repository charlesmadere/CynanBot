from .decTalkTtsManagerProvider import DecTalkTtsManagerProvider
from ..models.ttsProvider import TtsProvider


class UnrestrictedDecTalkTtsManagerProvider(DecTalkTtsManagerProvider):

    @property
    def ttsProvider(self) -> TtsProvider:
        return TtsProvider.UNRESTRICTED_DEC_TALK
