from dataclasses import dataclass
from datetime import datetime

from .glacialTtsData import GlacialTtsData


@dataclass(frozen = True)
class GlacialTtsFileReference:
    glacialTtsData: GlacialTtsData
    fileName: str
    filePath: str

    @property
    def storeDateTime(self) -> datetime:
        return self.glacialTtsData.storeDateTime
