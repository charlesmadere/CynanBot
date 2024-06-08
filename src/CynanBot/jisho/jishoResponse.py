from dataclasses import dataclass

from CynanBot.jisho.jishoData import JishoData
from CynanBot.jisho.jishoMeta import JishoMeta


@dataclass(frozen = True)
class JishoResponse():
    data: list[JishoData]
    meta: JishoMeta
