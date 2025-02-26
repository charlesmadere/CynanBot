from ..absPreferredTts import AbsPreferredTts
from ....streamElements.models.streamElementsVoice import StreamElementsVoice
from ....tts.models.ttsProvider import TtsProvider


class StreamElementsPreferredTts(AbsPreferredTts):

    def __init__(
        self,
        streamElementsVoice: StreamElementsVoice | None
    ):
        if streamElementsVoice is not None and not isinstance(streamElementsVoice, StreamElementsVoice):
            raise TypeError(f'streamElementsVoice argument is malformed: \"{streamElementsVoice}\"')

        self.__streamElementsVoiceEntry: StreamElementsVoice | None = streamElementsVoice

    @property
    def streamElementsVoiceEntry(self) -> StreamElementsVoice | None:
        return self.__streamElementsVoiceEntry


    @property
    def preferredTtsProvider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS
