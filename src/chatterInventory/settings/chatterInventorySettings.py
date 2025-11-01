from typing import Any, Final

from frozendict import frozendict

from .chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterItemType import ChatterItemType
from ..models.itemDetails.airStrikeItemDetails import AirStrikeItemDetails
from ..models.itemDetails.animalPetItemDetails import AnimalPetItemDetails
from ..models.itemDetails.bananaItemDetails import BananaItemDetails
from ..models.itemDetails.gashaponItemDetails import GashaponItemDetails
from ..models.itemDetails.grenadeItemDetails import GrenadeItemDetails
from ..models.itemDetails.tm36ItemDetails import Tm36ItemDetails
from ..models.itemDetails.voreItemDetails import VoreItemDetails
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class ChatterInventorySettings(ChatterInventorySettingsInterface):

    def __init__(
        self,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultAirStrikeItemDetails: AirStrikeItemDetails = AirStrikeItemDetails(
            maxDurationSeconds = 75,
            minDurationSeconds = 50,
            maxTargets = 13,
            minTargets = 9,
        ),
        defaultAnimalPetItemDetails: AnimalPetItemDetails = AnimalPetItemDetails(
            soundDirectory = 'sounds/animalPets',
        ),
        defaultBananaItemDetails: BananaItemDetails = BananaItemDetails(
            randomChanceEnabled = True,
            durationSeconds = 180, # 3 minutes
        ),
        defaultGashaponItemDetails: GashaponItemDetails = GashaponItemDetails(
            pullRates = frozendict({
                ChatterItemType.AIR_STRIKE: 0.0,
                ChatterItemType.ANIMAL_PET: 0.0,
                ChatterItemType.BANANA: 0.0,
                ChatterItemType.CASSETTE_TAPE: 0.0,
                ChatterItemType.GASHAPON: 0.0,
                ChatterItemType.GRENADE: 0.0,
                ChatterItemType.TM_36: 0.0,
                ChatterItemType.VORE: 0.0,
            }),
            iterations = 3,
        ),
        defaultGrenadeItemDetails: GrenadeItemDetails = GrenadeItemDetails(
            maxDurationSeconds = 48,
            minDurationSeconds = 32,
        ),
        defaultTm36ItemDetails: Tm36ItemDetails = Tm36ItemDetails(
            maxDurationSeconds = 300, # 5 minutes
            minDurationSeconds = 1800, # 30 minutes
        ),
        defaultVoreItemDetails: VoreItemDetails = VoreItemDetails(
            timeoutDurationSeconds = 86400, # 1 day
        ),
        defaultEnabledItemTypes: frozenset[ChatterItemType] = frozenset({
            ChatterItemType.AIR_STRIKE,
            ChatterItemType.BANANA,
            ChatterItemType.GRENADE,
        }),
    ):
        if not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultAirStrikeItemDetails, AirStrikeItemDetails):
            raise TypeError(f'defaultAirStrikeItemDetails argument is malformed: \"{defaultAirStrikeItemDetails}\"')
        elif not isinstance(defaultAnimalPetItemDetails, AnimalPetItemDetails):
            raise TypeError(f'defaultAnimalPetItemDetails argument is malformed: \"{defaultAnimalPetItemDetails}\"')
        elif not isinstance(defaultBananaItemDetails, BananaItemDetails):
            raise TypeError(f'defaultBananaItemDetails argument is malformed: \"{defaultBananaItemDetails}\"')
        elif not isinstance(defaultGashaponItemDetails, GashaponItemDetails):
            raise TypeError(f'defaultGashaponItemDetails argument is malformed: \"{defaultGashaponItemDetails}\"')
        elif not isinstance(defaultGrenadeItemDetails, GrenadeItemDetails):
            raise TypeError(f'grenadeItemDetails argument is malformed: \"{defaultGrenadeItemDetails}\"')
        elif not isinstance(defaultTm36ItemDetails, Tm36ItemDetails):
            raise TypeError(f'defaultTm36ItemDetails argument is malformed: \"{defaultTm36ItemDetails}\"')
        elif not isinstance(defaultVoreItemDetails, VoreItemDetails):
            raise TypeError(f'defaultVoreItemDetails argument is malformed: \"{defaultVoreItemDetails}\"')
        elif not isinstance(defaultEnabledItemTypes, frozenset):
            raise TypeError(f'defaultEnabledItemTypes argument is malformed: \"{defaultEnabledItemTypes}\"')

        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultAirStrikeItemDetails: Final[AirStrikeItemDetails] = defaultAirStrikeItemDetails
        self.__defaultAnimalPetItemDetails: Final[AnimalPetItemDetails] = defaultAnimalPetItemDetails
        self.__defaultBananaItemDetails: Final[BananaItemDetails] = defaultBananaItemDetails
        self.__defaultGashaponItemDetails: Final[GashaponItemDetails] = defaultGashaponItemDetails
        self.__defaultGrenadeItemDetails: Final[GrenadeItemDetails] = defaultGrenadeItemDetails
        self.__defaultTm36ItemDetails: Final[Tm36ItemDetails] = defaultTm36ItemDetails
        self.__defaultVoreItemDetails: Final[VoreItemDetails] = defaultVoreItemDetails
        self.__defaultEnabledItemTypes: Final[frozenset[ChatterItemType]] = defaultEnabledItemTypes

        self.__cache: dict[str, Any] | None = None

    async def areDiceRollsEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'diceRollsEnabled', True)

    async def clearCaches(self):
        self.__cache = None

    async def getAirStrikeItemDetails(self) -> AirStrikeItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('airStrikeItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseAirStrikeItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultAirStrikeItemDetails
        else:
            return itemDetails

    async def getAnimalPetItemDetails(self) -> AnimalPetItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('animalPetItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseAnimalPetItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultAnimalPetItemDetails
        else:
            return itemDetails

    async def getBananaItemDetails(self) -> BananaItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('bananaItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseBananaItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultBananaItemDetails
        else:
            return itemDetails

    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        jsonContents = await self.__readJson()
        enabledItemTypesStrings: list[str] | None = jsonContents.get('enabledItemTypes', None)

        if enabledItemTypesStrings is None:
            return self.__defaultEnabledItemTypes

        enabledItemTypes: set[ChatterItemType] = set()

        for enabledItemTypeString in enabledItemTypesStrings:
            enabledItemTypes.add(await self.__chatterInventoryMapper.requireItemType(enabledItemTypeString))

        return frozenset(enabledItemTypes)

    async def getGashaponItemDetails(self) -> GashaponItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('gashaponItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseGashaponItemDetails(itemDetailsJson)

        if itemDetails is None:
            itemDetails = self.__defaultGashaponItemDetails

        hydratedPullRates: dict[ChatterItemType, float] = dict(itemDetails.pullRates)

        for itemType in ChatterItemType:
            if itemType not in hydratedPullRates:
                hydratedPullRates[itemType] = 0.0

        return GashaponItemDetails(
            pullRates = frozendict(hydratedPullRates),
            iterations = itemDetails.iterations,
        )

    async def getGrenadeItemDetails(self) -> GrenadeItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('grenadeItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseGrenadeItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultGrenadeItemDetails
        else:
            return itemDetails

    async def getTm36ItemDetails(self) -> Tm36ItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('tm36ItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseTm36ItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultTm36ItemDetails
        else:
            return itemDetails

    async def getVoreItemDetails(self) -> VoreItemDetails:
        jsonContents = await self.__readJson()
        itemDetailsJson = jsonContents.get('voreItemDetails', None)
        itemDetails = await self.__chatterInventoryMapper.parseVoreItemDetails(itemDetailsJson)

        if itemDetails is None:
            return self.__defaultVoreItemDetails
        else:
            return itemDetails

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', False)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Chatter Inventory settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
