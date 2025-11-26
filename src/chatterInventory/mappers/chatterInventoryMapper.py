import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.animalPetItemDetails import AnimalPetItemDetails
from ..models.itemDetails.bananaItemDetails import BananaItemDetails
from ..models.itemDetails.gashaponItemDetails import GashaponItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..models.itemDetails.tm36ItemDetails import Tm36ItemDetails
from ..models.itemDetails.voreItemDetails import VoreItemDetails
from ...misc import utils as utils


class ChatterInventoryMapper(ChatterInventoryMapperInterface):

    def __init__(self):
        self.__itemTypeRegExes: Final[frozendict[ChatterItemType, Collection[Pattern]]] = self.__buildItemTypeRegExes()

    def __buildItemTypeRegExes(self) -> frozendict[ChatterItemType, Collection[Pattern]]:
        airStrike: FrozenList[Pattern] = FrozenList()
        airStrike.append(re.compile(r'^\s*air(?:\s+|_|-)?strikes?\s*$', re.IGNORECASE))
        airStrike.append(re.compile(r'^\s*tnt\'?s?\s*$', re.IGNORECASE))
        airStrike.freeze()

        animalPet: FrozenList[Pattern] = FrozenList()
        animalPet.append(re.compile(r'^\s*animal(?:\s+|_|-)?pets?\s*$', re.IGNORECASE))
        animalPet.append(re.compile(r'^\s*pet(?:\s+|_|-)?animals?\s*$', re.IGNORECASE))
        animalPet.append(re.compile(r'^\s*pets?\s*$', re.IGNORECASE))
        animalPet.freeze()

        banana: FrozenList[Pattern] = FrozenList()
        banana.append(re.compile(r'^\s*bananas?\s*$', re.IGNORECASE))
        banana.freeze()

        cassetteTape: FrozenList[Pattern] = FrozenList()
        cassetteTape.append(re.compile(r'^\s*cass?ett?es?\s*$', re.IGNORECASE))
        cassetteTape.append(re.compile(r'^\s*cass?ett?es?(?:\s+|_|-)?tapes?\s*$', re.IGNORECASE))
        cassetteTape.freeze()

        gashapon: FrozenList[Pattern] = FrozenList()
        gashapon.append(re.compile(r'^\s*gacha(?:pon)?s?\s*$', re.IGNORECASE))
        gashapon.append(re.compile(r'^\s*gasha(?:pon)?s?\s*$', re.IGNORECASE))
        gashapon.append(re.compile(r'^\s*lootbox\s*$', re.IGNORECASE))
        gashapon.append(re.compile(r'^\s*lootcrate\s*$', re.IGNORECASE))
        gashapon.append(re.compile(r'^\s*ガシャポン\s*$', re.IGNORECASE))
        gashapon.append(re.compile(r'^\s*ガチャポン\s*$', re.IGNORECASE))
        gashapon.freeze()

        grenade: FrozenList[Pattern] = FrozenList()
        grenade.append(re.compile(r'^\s*grenades?\s*$', re.IGNORECASE))
        grenade.append(re.compile(r'^\s*nades?\s*$', re.IGNORECASE))
        grenade.freeze()

        tm36: FrozenList[Pattern] = FrozenList()
        tm36.append(re.compile(r'^\s*tm(?:\s+|_|-)?36s?\s*$', re.IGNORECASE))
        tm36.freeze()

        vore: FrozenList[Pattern] = FrozenList()
        vore.append(re.compile(r'^\s*voars?\s*$', re.IGNORECASE))
        vore.append(re.compile(r'^\s*vores?\s*$', re.IGNORECASE))
        vore.freeze()

        return frozendict({
            ChatterItemType.AIR_STRIKE: airStrike,
            ChatterItemType.ANIMAL_PET: animalPet,
            ChatterItemType.BANANA: banana,
            ChatterItemType.CASSETTE_TAPE: cassetteTape,
            ChatterItemType.GASHAPON: gashapon,
            ChatterItemType.GRENADE: grenade,
            ChatterItemType.TM_36: tm36,
            ChatterItemType.VORE: vore,
        })

    async def parseAirStrikeItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> AirStrikeItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        maxDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'maxDurationSeconds')
        minDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'minDurationSeconds')
        maxTargets = utils.getIntFromDict(itemDetailsJson, 'maxTargets')
        minTargets = utils.getIntFromDict(itemDetailsJson, 'minTargets')

        return AirStrikeItemDetails(
            maxDurationSeconds = maxDurationSeconds,
            minDurationSeconds = minDurationSeconds,
            maxTargets = maxTargets,
            minTargets = minTargets,
        )

    async def parseAnimalPetItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> AnimalPetItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        soundDirectory = utils.getStrFromDict(itemDetailsJson, 'soundDirectory')

        return AnimalPetItemDetails(
            soundDirectory = soundDirectory,
        )

    async def parseBananaItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> BananaItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        randomChanceEnabled = utils.getBoolFromDict(itemDetailsJson, 'randomChanceEnabled')
        durationSeconds = utils.getIntFromDict(itemDetailsJson, 'durationSeconds')

        return BananaItemDetails(
            randomChanceEnabled = randomChanceEnabled,
            durationSeconds = durationSeconds,
        )

    async def parseGashaponItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> GashaponItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        pullRatesJson: dict[str, float | int] | Any | None = itemDetailsJson.get('pullRates', None)
        if not isinstance(pullRatesJson, dict) or len(pullRatesJson) == 0:
            return None

        iterations = utils.getIntFromDict(itemDetailsJson, 'iterations', fallback = 1)
        pullRates: dict[ChatterItemType, float] = dict()

        for itemTypeString, pullRate in pullRatesJson.items():
            itemType = await self.requireItemType(itemTypeString)

            if utils.isValidNum(pullRate):
                pullRate = max(min(pullRate, 1.0), 0.0)
            else:
                pullRate = 0.0

            pullRates[itemType] = float(pullRate)

        for itemType in ChatterItemType:
            if itemType not in pullRates:
                pullRates[itemType] = 0.0

        return GashaponItemDetails(
            pullRates = frozendict(pullRates),
            iterations = iterations,
        )

    async def parseGrenadeItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> GrenadeItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        maxDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'maxDurationSeconds')
        minDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'minDurationSeconds')

        return GrenadeItemDetails(
            maxDurationSeconds = maxDurationSeconds,
            minDurationSeconds = minDurationSeconds,
        )

    async def parseInventory(
        self,
        inventoryJson: dict[str, int | Any | None] | frozendict[str, int | Any | None] | Any | None,
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
        itemType: str | Any | None,
    ) -> ChatterItemType | None:
        if not utils.isValidStr(itemType):
            return None

        for itemTypeEnum, itemTypeRegExes in self.__itemTypeRegExes.items():
            for itemTypeRegEx in itemTypeRegExes:
                if itemTypeRegEx.fullmatch(itemType) is not None:
                    return itemTypeEnum

        return None

    async def parseTm36ItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> Tm36ItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        maxDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'maxDurationSeconds')
        minDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'minDurationSeconds')

        return Tm36ItemDetails(
            maxDurationSeconds = maxDurationSeconds,
            minDurationSeconds = minDurationSeconds,
        )

    async def parseVoreItemDetails(
        self,
        itemDetailsJson: dict[str, Any] | Any | None,
    ) -> VoreItemDetails | None:
        if not isinstance(itemDetailsJson, dict) or len(itemDetailsJson) == 0:
            return None

        timeoutDurationSeconds = utils.getIntFromDict(itemDetailsJson, 'timeoutDurationSeconds')

        return VoreItemDetails(
            timeoutDurationSeconds = timeoutDurationSeconds,
        )

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
            itemTypeAmount = max(0, inventory.get(itemType, 0))

            if itemTypeAmount >= 1:
                inventoryJson[itemTypeString] = itemTypeAmount

        return inventoryJson

    async def serializeItemType(
        self,
        itemType: ChatterItemType
    ) -> str:
        if not isinstance(itemType, ChatterItemType):
            raise TypeError(f'itemType argument is malformed: \"{itemType}\"')

        match itemType:
            case ChatterItemType.AIR_STRIKE: return 'air_strike'
            case ChatterItemType.ANIMAL_PET: return 'animal_pet'
            case ChatterItemType.BANANA: return 'banana'
            case ChatterItemType.CASSETTE_TAPE: return 'cassette_tape'
            case ChatterItemType.GASHAPON: return 'gashapon'
            case ChatterItemType.GRENADE: return 'grenade'
            case ChatterItemType.TM_36: return 'tm36'
            case ChatterItemType.VORE: return 'vore'
            case _: raise ValueError(f'Unknown ChatterItemType value: \"{itemType}\"')
