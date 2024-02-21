from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class TtsSettingsRepository(TtsSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getMaximumMessageSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxMessageSize', fallback = 200)

    async def getTtsDelayBetweenSeconds(self) -> float:
        jsonContents = await self.__readJson()

        ttsDelayBetweenSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'ttsDelayBetweenSeconds',
            fallback = 0.25
        )

        if ttsDelayBetweenSeconds < 0 or ttsDelayBetweenSeconds > 10:
            raise ValueError(f'ttsDelayBetweenSeconds is out of bounds: \"{ttsDelayBetweenSeconds}\"')

        return ttsDelayBetweenSeconds

    async def getTtsTimeoutSeconds(self) -> float:
        jsonContents = await self.__readJson()

        ttsTimeoutSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'ttsTimeoutSeconds',
            fallback = 10
        )

        if ttsTimeoutSeconds < 0 or ttsTimeoutSeconds > 30:
            raise ValueError(f'ttsTimeoutSeconds is out of bounds: \"{ttsTimeoutSeconds}\"')

        return ttsTimeoutSeconds

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = False)

    async def __readJson(self) -> Dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: Optional[Dict[str, Any]] = None

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
        decTalkPath = utils.getStrFromDict(jsonContents, 'decTalkPath', fallback = '')

        if not utils.isValidStr(decTalkPath):
            raise ValueError(f'\"decTalkPath\" value is malformed: \"{decTalkPath}\"')

        return decTalkPath
