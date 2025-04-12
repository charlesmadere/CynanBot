from typing import Any

from .crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface


class CrowdControlSettingsRepository(CrowdControlSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def areSoundsEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'soundsEnabled', True)

    async def clearCaches(self):
        self.__cache = None

    async def getActionLoopCooldownSeconds(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'actionLoopCooldownSeconds', 0.125)

    async def getMaxGigaShuffleCount(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxGigaShuffleCount', 16)

    async def getMaxHandleAttempts(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxHandleAttempts', 3)

    async def getMediaPlayerVolume(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', 75)

    async def getMessageCooldownSeconds(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'messageCooldownSeconds', float(1))

    async def getMinGigaShuffleCount(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'minGigaShuffleCount', 4)

    async def getSecondsToLive(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'secondsToLive', 300)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'enabled', True)

    async def isGigaShuffleEnabled(self):
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'gigaShuffleEnabled', True)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from crowd control settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
