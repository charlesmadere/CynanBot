from typing import Any

from ..misc import utils as utils
from ..storage.jsonReaderInterface import JsonReaderInterface
from .streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface


class StreamAlertsSettingsRepository(StreamAlertsSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getAlertsDelayBetweenSeconds(self) -> float:
        jsonContents = await self.__readJson()

        alertsDelayBetweenSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'alertsDelayBetweenSeconds',
            fallback = 1
        )

        if alertsDelayBetweenSeconds < 0 or alertsDelayBetweenSeconds > 30:
            raise ValueError(f'alertsDelayBetweenSeconds is out of bounds: \"{alertsDelayBetweenSeconds}\"')

        return alertsDelayBetweenSeconds

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from stream alerts settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
