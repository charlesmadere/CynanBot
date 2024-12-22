import pytest

from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.websocket.twitchWebsocketCondition import TwitchWebsocketCondition
from src.twitch.api.websocket.twitchWebsocketMessageType import TwitchWebsocketMessageType
from src.twitch.api.websocket.twitchWebsocketTransportMethod import TwitchWebsocketTransportMethod
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
    async def test_parseTransportMethod_withEmptyString(self):
        result = await self.websocketJsonMapper.parseTransportMethod('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withNone(self):
        result = await self.websocketJsonMapper.parseTransportMethod(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withConduit(self):
        result = await self.websocketJsonMapper.parseTransportMethod('conduit')
        assert result is TwitchWebsocketTransportMethod.CONDUIT

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWebhook(self):
        result = await self.websocketJsonMapper.parseTransportMethod('webhook')
        assert result is TwitchWebsocketTransportMethod.WEBHOOK

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWebsocket(self):
        result = await self.websocketJsonMapper.parseTransportMethod('websocket')
        assert result is TwitchWebsocketTransportMethod.WEBSOCKET

    @pytest.mark.asyncio
    async def test_parseTransportMethod_withWhitespaceString(self):
        result = await self.websocketJsonMapper.parseTransportMethod(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketChannelPointsVoting(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketChannelPointsVoting_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketChannelPointsVoting(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPollChoice_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketPollChoice(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketPollChoice_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketPollChoice(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCommunitySubGift_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketCommunitySubGift(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCommunitySubGift_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketCommunitySubGift(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketCondition_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketCondition(dict())
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
        result = await self.websocketJsonMapper.parseWebsocketCondition(None)
        assert result is None

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
    async def test_parseWebsocketOutcomePredictor_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseTwitchOutcomePredictor(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketOutcomePredictor_withNone(self):
        result = await self.websocketJsonMapper.parseTwitchOutcomePredictor(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketReward_withEmptyDictionary(self):
        result = await self.websocketJsonMapper.parseWebsocketReward(dict())
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketReward_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketReward(None)
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

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withEmptyString(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.websocketJsonMapper.requireTransportMethod('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withNone(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.websocketJsonMapper.requireTransportMethod(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withConduit(self):
        result = await self.websocketJsonMapper.requireTransportMethod('conduit')
        assert result is TwitchWebsocketTransportMethod.CONDUIT

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWebhook(self):
        result = await self.websocketJsonMapper.requireTransportMethod('webhook')
        assert result is TwitchWebsocketTransportMethod.WEBHOOK

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWebsocket(self):
        result = await self.websocketJsonMapper.requireTransportMethod('websocket')
        assert result is TwitchWebsocketTransportMethod.WEBSOCKET

    @pytest.mark.asyncio
    async def test_requireTransportMethod_withWhitespaceString(self):
        result: TwitchWebsocketTransportMethod | None = None

        with pytest.raises(Exception):
            result = await self.websocketJsonMapper.requireTransportMethod(' ')

        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withEmptyString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withNone(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withNotificationString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('notification')
        assert result is TwitchWebsocketMessageType.NOTIFICATION

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withRevocationString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('revocation')
        assert result is TwitchWebsocketMessageType.REVOCATION

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionKeepAliveString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('session_keepalive')
        assert result is TwitchWebsocketMessageType.KEEP_ALIVE

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionReconnectString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('session_reconnect')
        assert result is TwitchWebsocketMessageType.RECONNECT

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withSessionWelcomeString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType('session_welcome')
        assert result is TwitchWebsocketMessageType.WELCOME

    @pytest.mark.asyncio
    async def test_parseWebsocketMessageType_withWhitespaceString(self):
        result = await self.websocketJsonMapper.parseWebsocketMessageType(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withEmptyString(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.websocketJsonMapper.requireWebsocketMessageType('')

        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withNone(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.websocketJsonMapper.requireWebsocketMessageType(None)

        assert result is None

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withNotificationString(self):
        result = await self.websocketJsonMapper.requireWebsocketMessageType('notification')
        assert result is TwitchWebsocketMessageType.NOTIFICATION

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withRevocationString(self):
        result = await self.websocketJsonMapper.requireWebsocketMessageType('revocation')
        assert result is TwitchWebsocketMessageType.REVOCATION

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionKeepAliveString(self):
        result = await self.websocketJsonMapper.requireWebsocketMessageType('session_keepalive')
        assert result is TwitchWebsocketMessageType.KEEP_ALIVE

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionReconnectString(self):
        result = await self.websocketJsonMapper.requireWebsocketMessageType('session_reconnect')
        assert result is TwitchWebsocketMessageType.RECONNECT

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withSessionWelcomeString(self):
        result = await self.websocketJsonMapper.requireWebsocketMessageType('session_welcome')
        assert result is TwitchWebsocketMessageType.WELCOME

    @pytest.mark.asyncio
    async def test_requireWebsocketMessageType_withWhitespaceString(self):
        result: TwitchWebsocketMessageType | None = None

        with pytest.raises(ValueError):
            result = await self.websocketJsonMapper.requireWebsocketMessageType(' ')

        assert result is None

    def test_sanity(self):
        assert self.websocketJsonMapper is not None
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapper)
        assert isinstance(self.websocketJsonMapper, TwitchWebsocketJsonMapperInterface)
