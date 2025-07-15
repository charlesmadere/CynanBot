import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.websocket.twitchWebsocketJsonLoggingLevel import TwitchWebsocketJsonLoggingLevel
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface


class TestTwitchWebsocketJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository,
    )

    websocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
        timber = timber,
        twitchJsonMapper = jsonMapper,
    )

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withAllString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('all')
        assert result is TwitchWebsocketJsonLoggingLevel.ALL

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withLimitedString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('limited')
        assert result is TwitchWebsocketJsonLoggingLevel.LIMITED

    @pytest.mark.asyncio
    async def test_parseLoggingLevel_withNoneString(self):
        result = await self.websocketJsonMapper.parseLoggingLevel('none')
        assert result is TwitchWebsocketJsonLoggingLevel.NONE

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketDataBundle(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketDataBundle(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketEvent(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketEvent(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketSession(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketSession(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketSubscription(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketSubscription(None)
        assert result is None

    def test_sanity(self):
        assert self.websocketJsonMapper is not None
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapper)
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapperInterface)

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel(self):
        results: set[str] = set()

        for loggingLevel in TwitchWebsocketJsonLoggingLevel:
            results.add(await self.websocketJsonMapper.serializeLoggingLevel(loggingLevel))

        assert len(results) == len(TwitchWebsocketJsonLoggingLevel)

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withAll(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.ALL)
        assert result == 'all'

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withLimited(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.LIMITED)
        assert result == 'limited'

    @pytest.mark.asyncio
    async def test_serializeLoggingLevel_withNone(self):
        result = await self.websocketJsonMapper.serializeLoggingLevel(TwitchWebsocketJsonLoggingLevel.NONE)
        assert result == 'none'
