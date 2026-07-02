from typing import Final

import pytest

from src.twitch.api.models.twitchWebsocketCondition import TwitchWebsocketCondition
from src.twitch.api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from src.twitch.websocket.conditionBuilder.twitchWebsocketConditionBuilder import TwitchWebsocketConditionBuilder
from src.twitch.websocket.conditionBuilder.twitchWebsocketConditionBuilderInterface import \
    TwitchWebsocketConditionBuilderInterface
from src.twitch.websocket.twitchWebsocketUser import TwitchWebsocketUser


class TestTwitchWebsocketConditionBuilder:

    conditionBuilder: Final[TwitchWebsocketConditionBuilderInterface] = TwitchWebsocketConditionBuilder()

    @pytest.mark.asyncio
    async def test_build_withChannelChatMessage(self):
        websocketUser = TwitchWebsocketUser(
            userId = 'abc123',
            userName = 'stashiocat',
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId
        assert result.userId == websocketUser.userId

    @pytest.mark.asyncio
    async def test_build_withChannelChatNotification(self):
        websocketUser = TwitchWebsocketUser(
            userId = 'abc123',
            userName = 'stashiocat',
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CHAT_NOTIFICATION,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId
        assert result.userId == websocketUser.userId

    @pytest.mark.asyncio
    async def test_build_withChannelCustomPowerUpRedemption(self):
        websocketUser = TwitchWebsocketUser(
            userId = 'abc123',
            userName = 'smcharles',
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CUSTOM_POWER_UP_REDEMPTION,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId
        assert result.userId is None

    @pytest.mark.asyncio
    async def test_build_withChannelPointsRedemption(self):
        websocketUser = TwitchWebsocketUser(
            userId = 'def456',
            userName = 'imyt',
        )

        result = await self.conditionBuilder.build(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION,
            user = websocketUser,
        )

        assert isinstance(result, TwitchWebsocketCondition)
        assert result.broadcasterUserId == websocketUser.userId
        assert result.userId is None

    def test_sanity(self):
        assert self.conditionBuilder is not None
        assert isinstance(self.conditionBuilder, TwitchWebsocketConditionBuilder)
        assert isinstance(self.conditionBuilder, TwitchWebsocketConditionBuilderInterface)
