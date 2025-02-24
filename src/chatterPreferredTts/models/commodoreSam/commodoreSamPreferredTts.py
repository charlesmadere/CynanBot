from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class CommodoreSamPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
