from twitch.websocket.websocketNoticeType import WebsocketNoticeType


class TestTwitchWebsocketNoticeType():

    def test_fromStr_withAnnouncementString(self):
        result = WebsocketNoticeType.fromStr('announcement')
        assert result is WebsocketNoticeType.ANNOUNCEMENT

    def test_fromStr_withBitsBadgeTierString(self):
        result = WebsocketNoticeType.fromStr('bits_badge_tier')
        assert result is WebsocketNoticeType.BITS_BADGE_TIER

    def test_fromStr_withCharityDonationString(self):
        result = WebsocketNoticeType.fromStr('charity_donation')
        assert result is WebsocketNoticeType.CHARITY_DONATION

    def test_fromStr_withCommunitySubGiftString(self):
        result = WebsocketNoticeType.fromStr('community_sub_gift')
        assert result is WebsocketNoticeType.COMMUNITY_SUB_GIFT

    def test_fromStr_withGiftPaidUpgradeString(self):
        result = WebsocketNoticeType.fromStr('gift_paid_upgrade')
        assert result is WebsocketNoticeType.GIFT_PAID_UPGRADE

    def test_fromStr_withEmptyString(self):
        result = WebsocketNoticeType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = WebsocketNoticeType.fromStr(None)
        assert result is None

    def test_fromStr_withPayItForwardString(self):
        result = WebsocketNoticeType.fromStr('pay_it_forward')
        assert result is WebsocketNoticeType.PAY_IT_FORWARD

    def test_fromStr_withPrimePaidUpgradeString(self):
        result = WebsocketNoticeType.fromStr('prime_paid_upgrade')
        assert result is WebsocketNoticeType.PRIME_PAID_UPGRADE

    def test_fromStr_withRaidString(self):
        result = WebsocketNoticeType.fromStr('raid')
        assert result is WebsocketNoticeType.RAID

    def test_fromStr_withResubString(self):
        result = WebsocketNoticeType.fromStr('resub')
        assert result is WebsocketNoticeType.RE_SUB

        result = WebsocketNoticeType.fromStr('re_sub')
        assert result is WebsocketNoticeType.RE_SUB

    def test_fromStr_withSubString(self):
        result = WebsocketNoticeType.fromStr('sub')
        assert result is WebsocketNoticeType.SUB

    def test_fromStr_withSubGiftString(self):
        result = WebsocketNoticeType.fromStr('sub_gift')
        assert result is WebsocketNoticeType.SUB_GIFT

    def test_fromStr_withUnraidString(self):
        result = WebsocketNoticeType.fromStr('unraid')
        assert result is WebsocketNoticeType.UN_RAID

        result = WebsocketNoticeType.fromStr('un_raid')
        assert result is WebsocketNoticeType.UN_RAID

    def test_fromStr_withWhitespaceString(self):
        result = WebsocketNoticeType.fromStr(' ')
        assert result is None
