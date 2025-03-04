from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class DecTalkFileReference:
    storeDateTime: datetime
    filePath: str
