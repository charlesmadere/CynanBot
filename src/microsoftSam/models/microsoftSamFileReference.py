from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class MicrosoftSamFileReference:
    storeDateTime: datetime
    filePath: str
