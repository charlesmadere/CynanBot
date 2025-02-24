from typing import Any

from .commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class CommodoreSamSettingsRepository(CommodoreSamSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getCommodoreSamExecutablePath(self) -> str | None:
        jsonContents = await self.__readJson()

        commodoreSamPath = utils.getStrFromDict(
            d = jsonContents,
            key = 'commodoreSamPath',
            fallback = '../commodoreSam/sam.exe'
        )

        return utils.cleanPath(commodoreSamPath)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 4)

    async def requireCommodoreSamExecutablePath(self) -> str:
        commodoreSamPath = await self.getCommodoreSamExecutablePath()

        if not utils.isValidStr(commodoreSamPath):
            raise ValueError(f'\"commodoreSamPath\" value is malformed: \"{commodoreSamPath}\"')

        return commodoreSamPath

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Commodore Sam settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
