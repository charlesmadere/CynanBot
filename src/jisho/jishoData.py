from dataclasses import dataclass

from .jishoAttribution import JishoAttribution
from .jishoJapaneseWord import JishoJapaneseWord
from .jishoJlptLevel import JishoJlptLevel
from .jishoSense import JishoSense


@dataclass(frozen = True)
class JishoData():
    isCommon: bool
    attribution: JishoAttribution | None
    japanese: list[JishoJapaneseWord]
    jlptLevels: list[JishoJlptLevel] | None
    senses: list[JishoSense]
    slug: str
