from typing import Any, Final

from .timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TimeoutActionSettings(TimeoutActionSettingsInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDieSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'dieSize', fallback = 20)

    async def getFailureProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'failureProbability', fallback = 0.24)

    async def getGrenadeAdditionalReverseProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'grenadeAdditionalReverseProbability', fallback = 0.09)

    async def getReverseProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'reverseProbability', fallback = 0.05)

    async def getTm36SplashDamageProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'tm36SplashDamageProbability', fallback = 0.30)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from timeout action settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
