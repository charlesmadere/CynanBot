from dataclasses import dataclass

from frozenlist import FrozenList

from .jishoData import JishoData
from .jishoMeta import JishoMeta


@dataclass(frozen = True)
class JishoResponse:
    data: FrozenList[JishoData]
    meta: JishoMeta
