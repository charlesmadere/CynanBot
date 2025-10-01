from typing import Any, Final

from .ttsChatterSettingsRepositoryInterface import TtsChatterSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsChatterSettingsRepository(TtsChatterSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

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
            raise IOError(f'Error reading from TTS Chatter settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useThreshold(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'useThreshold', fallback = True)

    async def ttsOffThreshold(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'ttsOffThreshold', fallback = 500)

    async def ttsOnThreshold(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'ttsOnThreshold', fallback = 10)

    async def useMessageQueueing(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'useMessageQueueing', fallback = True)

    async def subscriberOnly(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'subscriberOnly', fallback = True)
