from dataclasses import dataclass

from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel
from CynanBot.jisho.jishoSense import JishoSense


@dataclass(frozen = True)
class JishoData():
    isCommon: bool
    senses: list[JishoSense]
    jlpt: set[JishoJlptLevel] | None
    slug: str
