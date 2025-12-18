from typing import Any, Final

from .watchStreakSettingsInterface import WatchStreakSettingsInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class WatchStreakSettings(WatchStreakSettingsInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        defaultMinimumWatchStreakForTts: int = 3,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not utils.isValidInt(defaultMinimumWatchStreakForTts):
            raise TypeError(f'defaultMinimumWatchStreakForTts argument is malformed: \"{defaultMinimumWatchStreakForTts}\"')
        elif defaultMinimumWatchStreakForTts < 1 or defaultMinimumWatchStreakForTts > utils.getIntMaxSafeSize():
            raise ValueError(f'defaultMinimumWatchStreakForTts argument is out of bounds: {defaultMinimumWatchStreakForTts}')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultMinimumWatchStreakForTts: Final[int] = defaultMinimumWatchStreakForTts

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', False)

    async def getMinimumWatchStreakForTts(self) -> int:
        jsonContents = await self.__readJson()
        minimumWatchStreakForTts = jsonContents.get('minimumWatchStreakForTts', None)

        if utils.isValidInt(minimumWatchStreakForTts):
            return minimumWatchStreakForTts
        else:
            return self.__defaultMinimumWatchStreakForTts

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Watch Streak settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
