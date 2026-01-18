from dataclasses import dataclass

from frozenlist import FrozenList

from .jishoAttribution import JishoAttribution
from .jishoJapaneseWord import JishoJapaneseWord
from .jishoJlptLevel import JishoJlptLevel
from .jishoSense import JishoSense


@dataclass(frozen = True)
class JishoData:
    isCommon: bool
    japanese: FrozenList[JishoJapaneseWord]
    senses: FrozenList[JishoSense]
    jlptLevels: frozenset[JishoJlptLevel]
    attribution: JishoAttribution | None
    slug: str
