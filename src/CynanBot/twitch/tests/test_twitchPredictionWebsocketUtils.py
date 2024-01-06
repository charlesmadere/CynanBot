from typing import Optional

import pytest

from CynanBot.twitch.twitchPredictionWebsocketUtils import \
    TwitchPredictionWebsocketUtils
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TestTwitchPredictionWebsocketUtils():

    utils: TwitchPredictionWebsocketUtilsInterface = TwitchPredictionWebsocketUtils()

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPointsRedemption(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionBegin(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
        )

        assert result == 'prediction_begin'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionEnd(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = WebsocketSubscriptionType.CHANNEL_PREDICTION_END
        )

        assert result == 'prediction_end'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionLock(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
        )

        assert result == 'prediction_lock'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionProgress(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
        )

        assert result == 'prediction_progress'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelUpdate(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.CHANNEL_UPDATE
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withCheer(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.CHEER
            )

        assert result is None


    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withFollow(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.FOLLOW
            )

        assert result is None


    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withRaid(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.RAID
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscribe(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.SUBSCRIBE
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscriptionGift(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.SUBSCRIPTION_GIFT
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscriptionMessage(self):
        result: Optional[str] = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
            )

        assert result is None



