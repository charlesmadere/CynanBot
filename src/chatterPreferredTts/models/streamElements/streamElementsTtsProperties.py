from dataclasses import dataclass

from ..absTtsProperties import AbsTtsProperties
from ....streamElements.models.streamElementsVoice import StreamElementsVoice
from ....tts.models.ttsProvider import TtsProvider


@dataclass(frozen = True, slots = True)
class StreamElementsTtsProperties(AbsTtsProperties):
    voice: StreamElementsVoice | None

    @property
    def provider(self) -> TtsProvider:
        return TtsProvider.STREAM_ELEMENTS
