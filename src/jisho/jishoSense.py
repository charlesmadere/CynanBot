from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True)
class JishoSense:
    englishDefinitions: FrozenList[str]
    partsOfSpeech: FrozenList[str] | None
    tags: FrozenList[str] | None
