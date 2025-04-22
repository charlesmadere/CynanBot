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

        return utils.getStrFromDict(
            d = jsonContents,
            key = 'commodoreSamPath',
            fallback = '../commodoreSam/sam.exe'
        )

    async def __getIntOrNone(self, key: str) -> int | None:
        jsonContents = await self.__readJson()

        value: int | None = None
        if key in jsonContents and utils.isValidInt(jsonContents.get(key)):
            value = utils.getIntFromDict(jsonContents, key)

        return value

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 4)

    async def getMouthParameter(self) -> int | None:
        return await self.__getIntOrNone('mouth')

    async def getPitchParameter(self) -> int | None:
        return await self.__getIntOrNone('pitch')

    async def getSpeedParameter(self) -> int | None:
        return await self.__getIntOrNone('speed')

    async def getThroatParameter(self) -> int | None:
        return await self.__getIntOrNone('throat')

    async def requireCommodoreSamExecutablePath(self) -> str:
        commodoreSamPath = await self.getCommodoreSamExecutablePath()

        if not utils.isValidStr(commodoreSamPath):
            raise ValueError(f'\"commodoreSamPath\" value is missing/malformed: \"{commodoreSamPath}\"')

        return commodoreSamPath

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Commodore Sam settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'useDonationPrefix', fallback = False)
