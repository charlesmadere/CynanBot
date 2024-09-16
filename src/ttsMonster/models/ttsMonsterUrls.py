from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True)
class TtsMonsterUrls:
    urls: FrozenList[str]
    characterAllowance: int | None
    characterUsage: int | None
