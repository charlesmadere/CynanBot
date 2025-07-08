from src.twitch.api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType


class TestTwitchWebsocketSubscriptionType:

    def test_version(self):
        versions: list[str] = list()

        for subscriptionType in TwitchWebsocketSubscriptionType:
            versions.append(subscriptionType.version)

        assert len(versions) == len(TwitchWebsocketSubscriptionType)

    def test_version_withChannelChatMessage(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_CHAT_MESSAGE.version
        assert version == '1'

    def test_version_withChannelPointsRedemption(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION.version
        assert version == '1'

    def test_version_withChannelPollBegin(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN.version
        assert version == '1'

    def test_version_withChannelPollEnd(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_END.version
        assert version == '1'

    def test_version_withChannelPollProgress(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS.version
        assert version == '1'

    def test_version_withChannelPredictionBegin(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN.version
        assert version == '1'

    def test_version_withChannelPredictionEnd(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END.version
        assert version == '1'

    def test_version_withChannelPredictionLock(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK.version
        assert version == '1'

    def test_version_withChannelPredictionProgress(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS.version
        assert version == '1'

    def test_version_withChannelUpdate(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_UPDATE.version
        assert version == '2'

    def test_version_withCheer(self):
        version = TwitchWebsocketSubscriptionType.CHEER.version
        assert version == '1'

    def test_version_withFollow(self):
        version = TwitchWebsocketSubscriptionType.FOLLOW.version
        assert version == '2'

    def test_version_withRaid(self):
        version = TwitchWebsocketSubscriptionType.RAID.version
        assert version == '1'

    def test_version_withStreamOffline(self):
        version = TwitchWebsocketSubscriptionType.STREAM_OFFLINE.version
        assert version == '1'

    def test_version_withStreamOnline(self):
        version = TwitchWebsocketSubscriptionType.STREAM_ONLINE.version
        assert version == '1'

    def test_version_withSubscribe(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIBE.version
        assert version == '1'

    def test_version_withSubscriptionGift(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT.version
        assert version == '1'

    def test_version_withSubscriptionMessage(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE.version
        assert version == '1'

    def test_version_withUserUpdate(self):
        version = TwitchWebsocketSubscriptionType.USER_UPDATE.version
        assert version == '1'
