import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from src.twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface


class TestTwitchWebsocketJsonMapper():

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    twitchJsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    jsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
        timber = timber,
        twitchJsonMapper = twitchJsonMapper
    )

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketChannelPointsVoting(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withNone(self):
        result = await self.jsonMapper.parseWebsocketChannelPointsVoting(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPollChoice_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketPollChoice(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPollChoice_withNone(self):
        result = await self.jsonMapper.parseWebsocketPollChoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCommunitySubGift_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketCommunitySubGift(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCommunitySubGift_withNone(self):
        result = await self.jsonMapper.parseWebsocketCommunitySubGift(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCondition_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketCondition(dict())
        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId is None
        assert result.broadcasterUserLogin is None
        assert result.broadcasterUserName is None
        assert result.clientId is None
        assert result.fromBroadcasterUserId is None
        assert result.fromBroadcasterUserLogin is None
        assert result.fromBroadcasterUserName is None
        assert result.moderatorUserId is None
        assert result.moderatorUserLogin is None
        assert result.moderatorUserName is None
        assert result.rewardId is None
        assert result.toBroadcasterUserId is None
        assert result.toBroadcasterUserLogin is None
        assert result.toBroadcasterUserName is None
        assert result.userId is None
        assert result.userLogin is None
        assert result.userName is None

        broadcasterUserId: str | None = None

        with pytest.raises(Exception):
            broadcasterUserId = result.requireBroadcasterUserId()

        assert broadcasterUserId is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCondition_withNone(self):
        result = await self.jsonMapper.parseWebsocketCondition(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketDataBundle(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketDataBundle_withNone(self):
        result = await self.jsonMapper.parseWebsocketDataBundle(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketEvent(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketEvent_withNone(self):
        result = await self.jsonMapper.parseWebsocketEvent(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcome_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTwitchOutcome(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcome_withNone(self):
        result = await self.jsonMapper.parseTwitchOutcome(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcomePredictor_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTwitchOutcomePredictor(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcomePredictor_withNone(self):
        result = await self.jsonMapper.parseTwitchOutcomePredictor(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketReward_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketReward(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketReward_withNone(self):
        result = await self.jsonMapper.parseWebsocketReward(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withEmptyDictionary(self):
        result = await self.jsonMapper.parseTwitchWebsocketSession(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSession_withNone(self):
        result = await self.jsonMapper.parseTwitchWebsocketSession(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubGift_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketSubGift(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubGift_withNone(self):
        result = await self.jsonMapper.parseWebsocketSubGift(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withEmptyDictionary(self):
        result = await self.jsonMapper.parseWebsocketSubscription(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketSubscription_withNone(self):
        result = await self.jsonMapper.parseWebsocketSubscription(None)
        assert result is None

    def test_sanity(self):
        assert self.jsonMapper is not None
        assert isinstance(self.jsonMapper, TwitchWebsocketJsonMapperInterface)
