from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.aniv.anivSettingsRepositoryInterface import \
    AnivSettingsRepositoryInterface
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


class AnivSettingsRepository(AnivSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

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

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from aniv settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
