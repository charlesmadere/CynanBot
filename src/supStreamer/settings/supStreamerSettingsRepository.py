from typing import Any, Final

from .supStreamerSettingsRepositoryInterface import SupStreamerSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class SupStreamerSettingsRepository(SupStreamerSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def areCustomSupMessagesEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'customSupMessagesEnabled', fallback = False)

    async def clearCaches(self):
        self.__cache = None

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Sup Streamer settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
