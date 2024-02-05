from typing import Optional

import pytest

from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.websocket.twitchWebsocketJsonMapper import \
    TwitchWebsocketJsonMapper
from CynanBot.twitch.websocket.twitchWebsocketJsonMapperInterface import \
    TwitchWebsocketJsonMapperInterface


class TestTwitchWebsocketJsonMapper():

    timber: TimberInterface = TimberStub()

    jsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
        timber = timber
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
        assert result.getBroadcasterUserId() is None
        assert result.getBroadcasterUserLogin() is None
        assert result.getBroadcasterUserName() is None
        assert result.getClientId() is None
        assert result.getFromBroadcasterUserId() is None
        assert result.getFromBroadcasterUserLogin() is None
        assert result.getFromBroadcasterUserName() is None
        assert result.getModeratorUserId() is None
        assert result.getModeratorUserLogin() is None
        assert result.getModeratorUserName() is None
        assert result.getRewardId() is None
        assert result.getToBroadcasterUserId() is None
        assert result.getToBroadcasterUserLogin() is None
        assert result.getToBroadcasterUserName() is None
        assert result.getUserId() is None
        assert result.getUserLogin() is None
        assert result.getUserName() is None
        assert result.isAnonymous() is None

        broadcasterUserId: Optional[str] = None
        exception: Optional[Exception] = None

        try:
            broadcasterUserId = result.requireBroadcasterUserId()
        except Exception as e:
            exception = e

        assert broadcasterUserId is None
        assert isinstance(exception, Exception)

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
