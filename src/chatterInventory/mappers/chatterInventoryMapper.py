import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterItemType import ChatterItemType
from ...misc import utils as utils


class ChatterInventoryMapper(ChatterInventoryMapperInterface):

    def __init__(self):
        self.__itemTypeRegExes: Final[frozendict[ChatterItemType, Collection[Pattern]]] = self.__buildItemTypeRegExes()

    def __buildItemTypeRegExes(self) -> frozendict[ChatterItemType, Collection[Pattern]]:
        airStrike: FrozenList[Pattern] = FrozenList()
        airStrike.append(re.compile(r'^\s*air(?:\s+|_|-)?strikes?\s*$', re.IGNORECASE))
        airStrike.freeze()

        grenade: FrozenList[Pattern] = FrozenList()
        grenade.append(re.compile(r'^\s*grenades?\s*$', re.IGNORECASE))
        grenade.freeze()

        return frozendict({
            ChatterItemType.AIR_STRIKE: airStrike,
            ChatterItemType.GRENADE: grenade,
        })

    async def parseItemType(
        self,
        itemType: str | Any | None
    ) -> ChatterItemType | None:
        if not utils.isValidStr(itemType):
            return None

        for itemTypeEnum, itemTypeRegExes in self.__itemTypeRegExes.items():
            for itemTypeRegEx in itemTypeRegExes:
                if itemTypeRegEx.fullmatch(itemType) is not None:
                    return itemTypeEnum

        return None

    async def requireItemType(
        self,
        itemType: str | Any | None
    ) -> ChatterItemType:
        result = await self.parseItemType(itemType)

        if result is None:
            raise ValueError(f'Unable to parse \"{itemType}\" into ChatterItemType value!')

        return result

    async def serializeItemType(
        self,
        itemType: ChatterItemType
    ) -> str:
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')

        match itemType:
            case ChatterItemType.AIR_STRIKE: return 'air_strike'
            case ChatterItemType.GRENADE: return 'grenade'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{itemType}\"')
