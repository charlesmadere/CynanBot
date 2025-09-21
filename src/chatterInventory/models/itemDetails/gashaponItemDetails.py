from dataclasses import dataclass

from ..chatterItemType import ChatterItemType


@dataclass(frozen = True)
class GashaponItemDetails:
    pullRates: dict[ChatterItemType, float]
