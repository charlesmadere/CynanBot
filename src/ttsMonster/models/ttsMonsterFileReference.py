from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TtsMonsterFileReference:
    storeDateTime: datetime
    filePath: str
