from typing import Any, Final

from .chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ..mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from ..models.chatterItemType import ChatterItemType
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class ChatterInventorySettings(ChatterInventorySettingsInterface):

    def __init__(
        self,
        chatterInventoryMapper: ChatterInventoryMapperInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultEnabledItemTypes: frozenset[ChatterItemType] = frozenset({
            ChatterItemType.AIR_STRIKE,
            ChatterItemType.GRENADE,
        })
    ):
        if not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultEnabledItemTypes, frozenset):
            raise TypeError(f'defaultEnabledItemTypes argument is malformed: \"{defaultEnabledItemTypes}\"')

        self.__chatterInventoryMapper: Final[ChatterInventoryMapperInterface] = chatterInventoryMapper
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultEnabledItemTypes: Final[frozenset[ChatterItemType]] = defaultEnabledItemTypes

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getEnabledItemTypes(self) -> frozenset[ChatterItemType]:
        jsonContents = await self.__readJson()
        enabledItemTypesStrings: list[str] | None = jsonContents.get('enabledItemTypes', None)

        if enabledItemTypesStrings is None:
            return self.__defaultEnabledItemTypes

        enabledItemTypes: set[ChatterItemType] = set()

        for enabledItemTypeString in enabledItemTypesStrings:
            enabledItemTypes.add(await self.__chatterInventoryMapper.requireItemType(enabledItemTypeString))

        return frozenset(enabledItemTypes)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', True)

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
