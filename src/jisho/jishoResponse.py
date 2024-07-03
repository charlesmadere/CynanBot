from dataclasses import dataclass

from .jishoData import JishoData
from .jishoMeta import JishoMeta


@dataclass(frozen = True)
class JishoResponse():
    data: list[JishoData]
    meta: JishoMeta
