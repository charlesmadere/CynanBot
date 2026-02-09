from dataclasses import dataclass

from frozenlist import FrozenList

from .jishoAttribution import JishoAttribution
from .jishoJapaneseWord import JishoJapaneseWord
from .jishoJlptLevel import JishoJlptLevel
from .jishoSense import JishoSense


@dataclass(frozen = True, slots = True)
class JishoData:
    isCommon: bool
    japanese: FrozenList[JishoJapaneseWord]
    jlptLevels: FrozenList[JishoJlptLevel]
    senses: FrozenList[JishoSense]
    attribution: JishoAttribution | None
    slug: str
