from typing import Any

from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface


class TtsSettingsRepository(TtsSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getMaximumMessageSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxMessageSize', fallback = 500)

    async def getTtsTimeoutSeconds(self) -> float:
        jsonContents = await self.__readJson()

        ttsTimeoutSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'ttsTimeoutSeconds',
            fallback = 30
        )

        if ttsTimeoutSeconds < 5 or ttsTimeoutSeconds > 300:
            raise ValueError(f'ttsTimeoutSeconds is out of bounds: \"{ttsTimeoutSeconds}\"')

        return ttsTimeoutSeconds

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = False)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents

    async def requireDecTalkPath(self) -> str:
        jsonContents = await self.__readJson()

        decTalkPath = utils.getStrFromDict(
            d = jsonContents,
            key = 'decTalkPath',
            fallback = 'dectalk/say.exe'
        )

        if not utils.isValidStr(decTalkPath):
            raise ValueError(f'\"decTalkPath\" value is malformed: \"{decTalkPath}\"')

        return decTalkPath
