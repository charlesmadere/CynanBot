from ..absPreferredTts import AbsPreferredTts
from ....tts.models.ttsProvider import TtsProvider


class CommodoreSamPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.COMMODORE_SAM
