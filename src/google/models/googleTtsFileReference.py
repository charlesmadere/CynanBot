from dataclasses import dataclass


@dataclass(frozen = True)
class GoogleTtsFileReference:
    filePath: str
