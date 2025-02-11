from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterFileReference:
    filePath: str
