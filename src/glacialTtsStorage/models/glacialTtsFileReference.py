from dataclasses import dataclass

from .glacialTtsData import GlacialTtsData


@dataclass(frozen = True)
class GlacialTtsFileReference:
    glacialTtsData: GlacialTtsData
    fileName: str
    filePath: str
