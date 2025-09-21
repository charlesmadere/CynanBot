from dataclasses import dataclass

from frozendict import frozendict

from ..chatterItemType import ChatterItemType


@dataclass(frozen = True)
class GashaponItemDetails:
    pullRates: frozendict[ChatterItemType, float]
    iterations: int

    def __getitem__(self, item: ChatterItemType) -> float:
        if not isinstance(item, ChatterItemType):
            raise TypeError(f'item argument is malformed: \"{item}\"')

        return self.pullRates.get(item, 0.0)
