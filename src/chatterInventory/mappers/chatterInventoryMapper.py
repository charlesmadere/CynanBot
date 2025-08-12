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
        airStrike.append(re.compile(r'^\s*tnt\'?s?\s*$', re.IGNORECASE))
        airStrike.freeze()

        banana: FrozenList[Pattern] = FrozenList()
        banana.append(re.compile(r'^\s*bananas?\s*$', re.IGNORECASE))
        banana.freeze()

        cassetteTape: FrozenList[Pattern] = FrozenList()
        cassetteTape.append(re.compile(r'^\s*cass?ett?es?\s*$', re.IGNORECASE))
        cassetteTape.append(re.compile(r'^\s*cass?ett?es?(?:\s+|_|-)?tapes?\s*$', re.IGNORECASE))
        cassetteTape.freeze()

        grenade: FrozenList[Pattern] = FrozenList()
        grenade.append(re.compile(r'^\s*grenades?\s*$', re.IGNORECASE))
        grenade.freeze()

        return frozendict({
            ChatterItemType.AIR_STRIKE: airStrike,
            ChatterItemType.BANANA: banana,
            ChatterItemType.CASSETTE_TAPE: cassetteTape,
            ChatterItemType.GRENADE: grenade,
        })

    async def parseInventory(
        self,
        inventoryJson: dict[str, int | Any | None] | frozendict[str, int | Any | None] | Any | None
    ) -> frozendict[ChatterItemType, int]:
        if not isinstance(inventoryJson, dict):
            inventoryJson = dict()

        inventory: dict[ChatterItemType, int] = dict()

        for itemType in ChatterItemType:
            itemTypeString = await self.serializeItemType(itemType)
            amount: int | Any | None = inventoryJson.get(itemTypeString, 0)

            if not utils.isValidInt(amount) or amount < 0:
                amount = 0

            inventory[itemType] = amount

        return frozendict(inventory)

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

    async def serializeInventory(
        self,
        inventory: dict[ChatterItemType, int] | frozendict[ChatterItemType, int]
    ) -> dict[str, int]:
        if not isinstance(inventory, dict):
            raise TypeError(f'inventory argument is malformed: \"{inventory}\"')

        inventoryJson: dict[str, int] = dict()

        for itemType in ChatterItemType:
            itemTypeString = await self.serializeItemType(itemType)
            inventoryJson[itemTypeString] = max(0, inventory.get(itemType, 0))

        return inventoryJson

    async def serializeItemType(
        self,
        itemType: ChatterItemType
    ) -> str:
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')

        match itemType:
            case ChatterItemType.AIR_STRIKE: return 'air_strike'
            case ChatterItemType.BANANA: return 'banana'
            case ChatterItemType.CASSETTE_TAPE: return 'cassette_tape'
            case ChatterItemType.GRENADE: return 'grenade'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{itemType}\"')
