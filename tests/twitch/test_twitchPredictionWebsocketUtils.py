from typing import Any, Final

import pytest

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.twitch.api.models.twitchOutcome import TwitchOutcome
from src.twitch.api.models.twitchOutcomeColor import TwitchOutcomeColor
from src.twitch.api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from src.twitch.twitchPredictionWebsocketUtils import TwitchPredictionWebsocketUtils
from src.twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface


class TestTwitchPredictionWebsocketUtils:

    timber: Final[TimberInterface] = TimberStub()

    utils: Final[TwitchPredictionWebsocketUtilsInterface] = TwitchPredictionWebsocketUtils(
        timber = timber,
    )

    @pytest.mark.asyncio
    async def test_outcomesToEventDataArray(self):
        outcomes: list[TwitchOutcome] = [
            TwitchOutcome(
                topPredictors = None,
                channelPoints = 0,
                users = 0,
                outcomeId = 'abc',
                title = 'Whomp',
                color = TwitchOutcomeColor.BLUE,
            ),
            TwitchOutcome(
                topPredictors = None,
                channelPoints = 5,
                users = 1,
                outcomeId = 'def',
                title = 'Thwomp',
                color = TwitchOutcomeColor.BLUE,
            ),
            TwitchOutcome(
                topPredictors = None,
                channelPoints = 10,
                users = 2,
                outcomeId = 'ghi',
                title = 'Boo',
                color = TwitchOutcomeColor.BLUE,
            ),
            TwitchOutcome(
                topPredictors = None,
                channelPoints = 15,
                users = 3,
                outcomeId = 'jkl',
                title = 'Bob-omb',
                color = TwitchOutcomeColor.BLUE,
            ),
        ]

        result = await self.utils.outcomesToEventDataArray(outcomes)
        assert isinstance(result, list)
        assert len(result) == 4

        assert len(result[0]) == 5
        assert result[0]['channelPoints'] == 15
        assert result[0]['color']['red'] == 54
        assert result[0]['color']['green'] == 162
        assert result[0]['color']['blue'] == 235
        assert result[0]['outcomeId'] == 'jkl'
        assert result[0]['title'] == 'Bob-omb'
        assert result[0]['users'] == 3

        assert len(result[1]) == 5
        assert result[1]['channelPoints'] == 10
        assert result[1]['color']['red'] == 255
        assert result[1]['color']['green'] == 99
        assert result[1]['color']['blue'] == 132
        assert result[1]['outcomeId'] == 'ghi'
        assert result[1]['title'] == 'Boo'
        assert result[1]['users'] == 2

        assert len(result[2]) == 5
        assert result[2]['channelPoints'] == 5
        assert result[2]['color']['red'] == 255
        assert result[2]['color']['green'] == 127
        assert result[2]['color']['blue'] == 0
        assert result[2]['outcomeId'] == 'def'
        assert result[2]['title'] == 'Thwomp'
        assert result[2]['users'] == 1

        assert len(result[3]) == 5
        assert result[3]['channelPoints'] == 0
        assert result[3]['color']['red'] == 127
        assert result[3]['color']['green'] == 255
        assert result[3]['color']['blue'] == 0
        assert result[3]['outcomeId'] == 'abc'
        assert result[3]['title'] == 'Whomp'
        assert result[3]['users'] == 0

    @pytest.mark.asyncio
    async def test_outcomesToEventDataArray_withEmptyList(self):
        result: list[dict[str, Any]] | None = None
        outcomes: list[TwitchOutcome] = list()

        with pytest.raises(TypeError):
            result = await self.utils.outcomesToEventDataArray(
                outcomes = outcomes
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_outcomeColorToEventData_withBlue(self):
        result = await self.utils.outcomeColorToEventData(TwitchOutcomeColor.BLUE)
        assert isinstance(result, dict)
        assert len(result) == 3
        assert result['red'] == 54
        assert result['green'] == 162
        assert result['blue'] == 235

    @pytest.mark.asyncio
    async def test_outcomeColorToEventData_withPink(self):
        result = await self.utils.outcomeColorToEventData(TwitchOutcomeColor.PINK)
        assert isinstance(result, dict)
        assert len(result) == 3
        assert result['red'] == 255
        assert result['green'] == 99
        assert result['blue'] == 132

    def test_sanity(self):
        assert self.utils is not None
        assert isinstance(self.utils, TwitchPredictionWebsocketUtils)
        assert isinstance(self.utils, TwitchPredictionWebsocketUtilsInterface)

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelChatMessage(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelCheer(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_CHEER
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPointsRedemption(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionBegin(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN
        )

        assert result == 'prediction_begin'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionEnd(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END
        )

        assert result == 'prediction_end'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionLock(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK
        )

        assert result == 'prediction_lock'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelPredictionProgress(self):
        result = await self.utils.websocketSubscriptionTypeToString(
            subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS
        )

        assert result == 'prediction_progress'

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withChannelUpdate(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.CHANNEL_UPDATE
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withFollow(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.FOLLOW
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withRaid(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.RAID
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscribe(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIBE
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscriptionGift(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT
            )

        assert result is None

    @pytest.mark.asyncio
    async def test_websocketSubscriptionTypeToString_withSubscriptionMessage(self):
        result: str | None = None

        with pytest.raises(ValueError):
            result = await self.utils.websocketSubscriptionTypeToString(
               subscriptionType = TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE
            )

        assert result is None
