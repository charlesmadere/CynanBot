from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterFileReference:
    fileName: str
    filePath: str
