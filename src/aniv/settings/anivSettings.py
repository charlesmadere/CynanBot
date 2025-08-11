from typing import Any, Final

from .anivSettingsInterface import AnivSettingsInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class AnivSettings(AnivSettingsInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def areCopyMessageTimeoutsEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'copyMessageTimeoutsEnabled', fallback = True)

    async def clearCaches(self):
        self.__settingsCache = None

    async def getCopyMessageMaxAgeSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'copyMessageMaxAgeSeconds', fallback = 30)

    async def getCopyMessageTimeoutProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'copyMessageTimeoutProbability', fallback = 0.69)

    async def getCopyMessageTimeoutSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'copyMessageTimeoutSeconds', fallback = 30)

    async def getCopyMessageTimeoutMaxSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'copyMessageTimeoutMaxSeconds', fallback = 300)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from aniv settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
