from dataclasses import dataclass

from CynanBot.jisho.jishoAttribution import JishoAttribution
from CynanBot.jisho.jishoJapaneseWord import JishoJapaneseWord
from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoSense import JishoSense


@dataclass(frozen = True)
class JishoData():
    isCommon: bool
    attribution: JishoAttribution
    japanese: list[JishoJapaneseWord]
    jlptLevels: list[JishoJlptLevel] | None
    senses: list[JishoSense]
    slug: str
