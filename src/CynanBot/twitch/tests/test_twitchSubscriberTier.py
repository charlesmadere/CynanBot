import pytest

from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TestTwitchSubscriberTier():

    def test_fromStr_withPrimeString(self):
        result = TwitchSubscriberTier.fromStr('prime')
        assert result is TwitchSubscriberTier.PRIME

    def test_fromStr_with1000String(self):
        result = TwitchSubscriberTier.fromStr('1000')
        assert result is TwitchSubscriberTier.TIER_ONE

    def test_fromStr_with2000String(self):
        result = TwitchSubscriberTier.fromStr('2000')
        assert result is TwitchSubscriberTier.TIER_TWO

    def test_fromStr_with3000String(self):
        result = TwitchSubscriberTier.fromStr('3000')
        assert result is TwitchSubscriberTier.TIER_THREE

    def test_fromStr_withEmptyString(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(TypeError):
            result = TwitchSubscriberTier.fromStr('')

        assert result is None

    def test_fromStr_withNone(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(TypeError):
            result = TwitchSubscriberTier.fromStr('')

        assert result is None

    def test_fromStr_withWhitespaceString(self):
        result: TwitchSubscriberTier | None = None

        with pytest.raises(TypeError):
            result = TwitchSubscriberTier.fromStr('')

        assert result is None
