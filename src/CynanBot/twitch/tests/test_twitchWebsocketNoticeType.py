from CynanBot.twitch.api.websocket.twitchWebsocketNoticeType import \
    TwitchWebsocketNoticeType


class TestTwitchWebsocketNoticeType():

    def test_fromStr_withAnnouncementString(self):
        result = TwitchWebsocketNoticeType.fromStr('announcement')
        assert result is TwitchWebsocketNoticeType.ANNOUNCEMENT

    def test_fromStr_withBitsBadgeTierString(self):
        result = TwitchWebsocketNoticeType.fromStr('bits_badge_tier')
        assert result is TwitchWebsocketNoticeType.BITS_BADGE_TIER

    def test_fromStr_withCharityDonationString(self):
        result = TwitchWebsocketNoticeType.fromStr('charity_donation')
        assert result is TwitchWebsocketNoticeType.CHARITY_DONATION

    def test_fromStr_withCommunitySubGiftString(self):
        result = TwitchWebsocketNoticeType.fromStr('community_sub_gift')
        assert result is TwitchWebsocketNoticeType.COMMUNITY_SUB_GIFT

    def test_fromStr_withGiftPaidUpgradeString(self):
        result = TwitchWebsocketNoticeType.fromStr('gift_paid_upgrade')
        assert result is TwitchWebsocketNoticeType.GIFT_PAID_UPGRADE

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketNoticeType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = TwitchWebsocketNoticeType.fromStr(None)
        assert result is None

    def test_fromStr_withPayItForwardString(self):
        result = TwitchWebsocketNoticeType.fromStr('pay_it_forward')
        assert result is TwitchWebsocketNoticeType.PAY_IT_FORWARD

    def test_fromStr_withPrimePaidUpgradeString(self):
        result = TwitchWebsocketNoticeType.fromStr('prime_paid_upgrade')
        assert result is TwitchWebsocketNoticeType.PRIME_PAID_UPGRADE

    def test_fromStr_withRaidString(self):
        result = TwitchWebsocketNoticeType.fromStr('raid')
        assert result is TwitchWebsocketNoticeType.RAID

    def test_fromStr_withResubString(self):
        result = TwitchWebsocketNoticeType.fromStr('resub')
        assert result is TwitchWebsocketNoticeType.RE_SUB

    def test_fromStr_withSubString(self):
        result = TwitchWebsocketNoticeType.fromStr('sub')
        assert result is TwitchWebsocketNoticeType.SUB

    def test_fromStr_withSubGiftString(self):
        result = TwitchWebsocketNoticeType.fromStr('sub_gift')
        assert result is TwitchWebsocketNoticeType.SUB_GIFT

    def test_fromStr_withUnraidString(self):
        result = TwitchWebsocketNoticeType.fromStr('unraid')
        assert result is TwitchWebsocketNoticeType.UN_RAID

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketNoticeType.fromStr(' ')
        assert result is None
