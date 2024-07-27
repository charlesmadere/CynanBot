from src.twitch.api.twitchRewardRedemptionStatus import \
    TwitchRewardRedemptionStatus


class TestTwitchWebsocketRewardRedemptionStatus:

    def test_fromStr_withCanceledString(self):
        result = TwitchRewardRedemptionStatus.fromStr('canceled')
        assert result is TwitchRewardRedemptionStatus.CANCELED

    def test_fromStr_withFulfilledString(self):
        result = TwitchRewardRedemptionStatus.fromStr('fulfilled')
        assert result is TwitchRewardRedemptionStatus.FULFILLED

    def test_fromStr_withEmptyString(self):
        result = TwitchRewardRedemptionStatus.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = TwitchRewardRedemptionStatus.fromStr(None)
        assert result is None

    def test_fromStr_withUnfulfilledString(self):
        result = TwitchRewardRedemptionStatus.fromStr('unfulfilled')
        assert result is TwitchRewardRedemptionStatus.UNFULFILLED

    def test_fromStr_withUnknownString(self):
        result = TwitchRewardRedemptionStatus.fromStr('unknown')
        assert result is TwitchRewardRedemptionStatus.UNKNOWN

    def test_fromStr_withWhitespaceString(self):
        result = TwitchRewardRedemptionStatus.fromStr(' ')
        assert result is None
