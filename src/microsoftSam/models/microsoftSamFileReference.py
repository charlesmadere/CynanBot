from dataclasses import dataclass
from datetime import datetime

from .microsoftSamVoice import MicrosoftSamVoice


@dataclass(frozen = True)
class MicrosoftSamFileReference:
    storeDateTime: datetime
    voice: MicrosoftSamVoice
    filePath: str
