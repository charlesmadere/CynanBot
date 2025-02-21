from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class MicrosoftSamPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.MICROSOFT_SAM
