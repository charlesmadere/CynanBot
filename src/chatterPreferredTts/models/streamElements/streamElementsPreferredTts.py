from typing import Final

from ..absTtsProperties import AbsTtsProperties
from ....streamElements.models.streamElementsVoice import StreamElementsVoice
from ....tts.models.ttsProvider import TtsProvider


class StreamElementsTtsProperties(AbsTtsProperties):

    def __init__(
        self,
        voice: StreamElementsVoice | None
    ):
        if voice is not None and not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice is malformed: \"{voice}\"')

        self.__voice: Final[StreamElementsVoice | None] = voice

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS

    @property
    def voice(self) -> StreamElementsVoice | None:
        return self.__voice
