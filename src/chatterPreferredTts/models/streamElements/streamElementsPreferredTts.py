from ..absPreferredTts import AbsPreferredTts
from ....streamElements.models.streamElementsVoice import StreamElementsVoice
from ....tts.models.ttsProvider import TtsProvider


class StreamElementsPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        voice: StreamElementsVoice | None
    ):
        if voice is not None and not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice is malformed: \"{voice}\"')

        self.__voice: StreamElementsVoice | None = voice

    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS

    @property
    def voice(self) -> StreamElementsVoice | None:
        return self.__voice
