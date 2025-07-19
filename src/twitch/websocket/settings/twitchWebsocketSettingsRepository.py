from typing import Any, Final

from .twitchWebsocketSettingsRepositoryInterface import TwitchWebsocketSettingsRepositoryInterface
from ..twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from ..twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from ....misc import utils as utils
from ....storage.jsonReaderInterface import JsonReaderInterface


class TwitchWebsocketSettingsRepository(TwitchWebsocketSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        defaultJsonLoggingLevel: TwitchWebsocketJsonLoggingLevel = TwitchWebsocketJsonLoggingLevel.LIMITED,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise TypeError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
        elif not isinstance(defaultJsonLoggingLevel, TwitchWebsocketJsonLoggingLevel):
            raise TypeError(f'defaultJsonLoggingLevel argument is malformed: \"{defaultJsonLoggingLevel}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__twitchWebsocketJsonMapper: Final[TwitchWebsocketJsonMapperInterface] = twitchWebsocketJsonMapper
        self.__defaultJsonLoggingLevel: Final[TwitchWebsocketJsonLoggingLevel] = defaultJsonLoggingLevel

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getLoggingLevel(self) -> TwitchWebsocketJsonLoggingLevel:
        jsonContents = await self.__readJson()

        loggingLevelStr = utils.getStrFromDict(
            d = jsonContents,
            key = 'loggingLevel',
            fallback = await self.__twitchWebsocketJsonMapper.serializeLoggingLevel(self.__defaultJsonLoggingLevel)
        )

        return await self.__twitchWebsocketJsonMapper.parseLoggingLevel(loggingLevelStr)

    async def isChatEventToCheerEventSubscriptionFallbackEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'chatEventToCheerEventSubscriptionFallbackEnabled', fallback = True)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Twitch Websocket settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
