from ..absPreferredTts import AbsPreferredTts
from ....tts.ttsProvider import TtsProvider


class StreamElementsPreferredTts(AbsPreferredTts):

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS
