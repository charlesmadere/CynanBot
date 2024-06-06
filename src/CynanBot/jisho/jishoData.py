from dataclasses import dataclass

from CynanBot.jisho.jishoJlptLevel import JishoJlptLevel


@dataclass(frozen = True)
class JishoData():
    isCommon: bool
    jlpt: set[JishoJlptLevel] | None
    slug: str
