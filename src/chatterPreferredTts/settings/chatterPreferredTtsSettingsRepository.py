from typing import Any

from .chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class ChatterPreferredTtsSettingsRepository(ChatterPreferredTtsSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = True)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from Chatter Preferred TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
