from dataclasses import dataclass

from .streamElementsVoice import StreamElementsVoice


@dataclass(frozen = True)
class StreamElementsMessage:
    message: str
    voice: StreamElementsVoice
