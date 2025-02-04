import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface


class TestTwitchWebsocketJsonMapper:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    jsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    websocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
        timber = timber,
        twitchJsonMapper = jsonMapper
    )

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
    async def test_parseWebsocketOutcome_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseTwitchOutcome(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcome_withNone(self):
        result = await self.websocketJsonMapper.parseTwitchOutcome(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseTwitchWebsocketSession(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withNone(self):
        result = await self.websocketJsonMapper.parseTwitchWebsocketSession(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubGift_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketSubGift(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubGift_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketSubGift(None)
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
