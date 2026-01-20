from dataclasses import dataclass

from frozenlist import FrozenList


@dataclass(frozen = True, slots = True)
class JishoSense:
    englishDefinitions: FrozenList[str]
    partsOfSpeech: FrozenList[str]
    tags: FrozenList[str]
