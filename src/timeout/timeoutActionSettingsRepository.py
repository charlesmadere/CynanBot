from typing import Any

from .timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface


class TimeoutActionSettingsRepository(TimeoutActionSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getActionLoopCooldownSeconds(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'actionLoopCooldownSeconds', 0.25)

    async def getBullyTimeToLiveDays(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'bullyTimeToLiveDays', 14)

    async def getDieSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'dieSize', 20)

    async def getFailureProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'failureProbability', 0.20)

    async def getGrenadeAdditionalReverseProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'grenadeAdditionalReverseProbability', 0.09)

    async def getMassiveTimeoutHoursTransitionPoint(self) -> int | None:
        jsonContents = await self.__readJson()

        massiveTimeoutHoursTransitionPoint: int | None = None
        if 'massiveTimeoutHoursTransitionPoint' in jsonContents and utils.isValidInt(jsonContents.get('massiveTimeoutHoursTransitionPoint')):
            massiveTimeoutHoursTransitionPoint = utils.getIntFromDict(jsonContents, 'massiveTimeoutHoursTransitionPoint')

        return massiveTimeoutHoursTransitionPoint

    async def getMaxBullyFailureOccurrences(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxBullyFailureOccurrences', 3)

    async def getMaxBullyFailureProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'maxBullyFailureProbability', 0.70)

    async def getReverseProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'reverseProbability', 0.05)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from timeout cheer action settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
