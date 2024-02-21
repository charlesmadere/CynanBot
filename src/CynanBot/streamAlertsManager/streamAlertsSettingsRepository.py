from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.streamAlertsManager.streamAlertsSettingsRepositoryInterface import \
    StreamAlertsSettingsRepositoryInterface


class StreamAlertsSettingsRepository(StreamAlertsSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: Optional[Dict[str, Any]] = None

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

    async def __readJson(self) -> Dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: Optional[Dict[str, Any]] = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from stream alerts settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
