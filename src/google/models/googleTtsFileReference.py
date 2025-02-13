from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class GoogleTtsFileReference:
    storeDateTime: datetime
    filePath: str
