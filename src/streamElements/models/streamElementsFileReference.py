from dataclasses import dataclass
from datetime import datetime

from .streamElementsVoice import StreamElementsVoice


@dataclass(frozen = True, slots = True)
class StreamElementsFileReference:
    storeDateTime: datetime
    filePath: str
    voice: StreamElementsVoice
