from typing import Any, Final

from .twitchWebsocketSettingsRepositoryInterface import TwitchWebsocketSettingsRepositoryInterface
from ..twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from ..twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from ...api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from ...api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ....misc import utils as utils
from ....storage.jsonReaderInterface import JsonReaderInterface


class TwitchWebsocketSettingsRepository(TwitchWebsocketSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        twitchJsonMapper: TwitchJsonMapperInterface,
        twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface,
        defaultSubscriptionTypes: frozenset[TwitchWebsocketSubscriptionType] = frozenset({
            TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE,
            TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_END,
            TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END,
            TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS,
            TwitchWebsocketSubscriptionType.FOLLOW,
            TwitchWebsocketSubscriptionType.RAID,
            TwitchWebsocketSubscriptionType.SUBSCRIBE,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT,
            TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE,
        }),
        defaultJsonLoggingLevel: TwitchWebsocketJsonLoggingLevel = TwitchWebsocketJsonLoggingLevel.LIMITED,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(twitchJsonMapper, TwitchJsonMapperInterface):
            raise TypeError(f'twitchJsonMapper argument is malformed: \"{twitchJsonMapper}\"')
        elif not isinstance(twitchWebsocketJsonMapper, TwitchWebsocketJsonMapperInterface):
            raise TypeError(f'twitchWebsocketJsonMapper argument is malformed: \"{twitchWebsocketJsonMapper}\"')
        elif not isinstance(defaultSubscriptionTypes, frozenset):
            raise TypeError(f'defaultSubscriptionTypes argument is malformed: \"{defaultSubscriptionTypes}\"')
        elif not isinstance(defaultJsonLoggingLevel, TwitchWebsocketJsonLoggingLevel):
            raise TypeError(f'defaultJsonLoggingLevel argument is malformed: \"{defaultJsonLoggingLevel}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__twitchJsonMapper: Final[TwitchJsonMapperInterface] = twitchJsonMapper
        self.__twitchWebsocketJsonMapper: Final[TwitchWebsocketJsonMapperInterface] = twitchWebsocketJsonMapper
        self.__defaultSubscriptionTypes: Final[frozenset[TwitchWebsocketSubscriptionType]] = defaultSubscriptionTypes
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

    async def getSubscriptionTypes(self) -> frozenset[TwitchWebsocketSubscriptionType]:
        jsonContents = await self.__readJson()
        subscriptionTypesStrings: list[str] | None = jsonContents.get('subscriptionTypes', None)

        if subscriptionTypesStrings is None:
            return self.__defaultSubscriptionTypes

        subscriptionTypes: set[TwitchWebsocketSubscriptionType] = set()

        for subscriptionTypeString in subscriptionTypesStrings:
            subscriptionTypes.add(await self.__twitchJsonMapper.requireSubscriptionType(subscriptionTypeString))

        return frozenset(subscriptionTypes)

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
