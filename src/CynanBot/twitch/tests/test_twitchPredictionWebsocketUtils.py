from typing import Any, Dict, List, Optional

import pytest

from CynanBot.twitch.twitchPredictionWebsocketUtils import \
    TwitchPredictionWebsocketUtils
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketOutcomeColor import \
    WebsocketOutcomeColor
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TestTwitchPredictionWebsocketUtils():

    utils: TwitchPredictionWebsocketUtilsInterface = TwitchPredictionWebsocketUtils()

    @pytest.mark.asyncio
    async def test_websocketOutcomesToEventDataArray(self):
        result: Optional[List[Dict[str, Any]]] = None
        outcomes: List[WebsocketOutcome] = [
            WebsocketOutcome(
                channelPoints = 0,
                users = 0,
                outcomeId = 'abc',
                title = 'Whomp',
                color = WebsocketOutcomeColor.BLUE
            ),
            WebsocketOutcome(
                channelPoints = 5,
                users = 1,
                outcomeId = 'def',
                title = 'Thwomp',
                color = WebsocketOutcomeColor.BLUE
            ),
            WebsocketOutcome(
                channelPoints = 10,
                users = 2,
                outcomeId = 'ghi',
                title = 'Boo',
                color = WebsocketOutcomeColor.BLUE
            ),
            WebsocketOutcome(
                channelPoints = 15,
                users = 3,
                outcomeId = 'jkl',
                title = 'Bob-omb',
                color = WebsocketOutcomeColor.BLUE
            )
        ]

        result = await self.utils.websocketOutcomesToEventDataArray(outcomes)
        assert isinstance(result, List)
        assert len(result) == 4

        assert len(result[0]) == 4
        assert result[0]['channelPoints'] == 15
        assert result[0]['outcomeId'] == 'jkl'
        assert result[0]['title'] == 'Bob-omb'
        assert result[0]['users'] == 3

        assert len(result[1]) == 4
        assert result[1]['channelPoints'] == 10
        assert result[1]['outcomeId'] == 'ghi'
        assert result[1]['title'] == 'Boo'
        assert result[1]['users'] == 2

        assert len(result[2]) == 4
        assert result[2]['channelPoints'] == 5
        assert result[2]['outcomeId'] == 'def'
        assert result[2]['title'] == 'Thwomp'
        assert result[2]['users'] == 1

        assert len(result[3]) == 4
        assert result[3]['channelPoints'] == 0
        assert result[3]['outcomeId'] == 'abc'
        assert result[3]['title'] == 'Whomp'
        assert result[3]['users'] == 0

    @pytest.mark.asyncio
    async def test_websocketOutcomesToEventDataArray_withEmptyList(self):
        result: Optional[List[Dict[str, Any]]] = None
        outcomes: List[WebsocketOutcome] = list()

        with pytest.raises(ValueError):
            result = await self.utils.websocketOutcomesToEventDataArray(
                outcomes = outcomes
            )

        assert result is None

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
