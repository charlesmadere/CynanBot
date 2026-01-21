from dataclasses import dataclass
from datetime import datetime

from .microsoftTtsVoice import MicrosoftTtsVoice


@dataclass(frozen = True, slots = True)
class MicrosoftTtsFileReference:
    storeDateTime: datetime
    voice: MicrosoftTtsVoice
    filePath: str
