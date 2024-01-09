from CynanBot.twitch.websocket.twitchWebsocketRewardRedemptionStatus import \
    TwitchWebsocketRewardRedemptionStatus


class TestTwitchWebsocketRewardRedemptionStatus():

    def test_fromStr_withCanceledString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr('canceled')
        assert result is TwitchWebsocketRewardRedemptionStatus.CANCELED

    def test_fromStr_withFulfilledString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr('fulfilled')
        assert result is TwitchWebsocketRewardRedemptionStatus.FULFILLED

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr(None)
        assert result is None

    def test_fromStr_withUnfulfilledString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr('unfulfilled')
        assert result is TwitchWebsocketRewardRedemptionStatus.UNFULFILLED

    def test_fromStr_withUnknownString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr('unknown')
        assert result is TwitchWebsocketRewardRedemptionStatus.UNKNOWN

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketRewardRedemptionStatus.fromStr(' ')
        assert result is None
