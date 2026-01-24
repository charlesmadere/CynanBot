from dataclasses import dataclass

from frozendict import frozendict

from .gashaponItemPullRate import GashaponItemPullRate
from ..chatterItemType import ChatterItemType


@dataclass(frozen = True, slots = True)
class GashaponItemDetails:
    pullRates: frozendict[ChatterItemType, GashaponItemPullRate]

    def __getitem__(self, item: ChatterItemType) -> GashaponItemPullRate:
        if not isinstance(item, ChatterItemType):
            raise TypeError(f'item argument is malformed: \"{item}\"')

        return self.pullRates.get(item, GashaponItemPullRate(
            pullRate = 0.0,
            iterations = 0,
            maximumPullAmount = 0,
            minimumPullAmount = 0,
        ))
