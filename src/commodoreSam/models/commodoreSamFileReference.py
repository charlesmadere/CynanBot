from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class CommodoreSamFileReference:
    storeDateTime: datetime
    filePath: str
