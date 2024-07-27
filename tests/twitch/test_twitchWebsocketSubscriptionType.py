from src.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType


class TestTwitchWebsocketSubscriptionType:

    def test_fromStr_withChannelChannelPointsCustomRewardRedemptionString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.channel_points_custom_reward_redemption.add')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    def test_fromStr_withChannelPollBeginString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.poll.begin')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN

    def test_fromStr_withChannelPollEndString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.poll.end')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_END

    def test_fromStr_withChannelPollProgressString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.poll.progress')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    def test_fromStr_withChannelPredictionBeginString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.prediction.begin')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN

    def test_fromStr_withChannelPredictionEndString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.prediction.end')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END

    def test_fromStr_withChannelPredictionLockString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.prediction.lock')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK

    def test_fromStr_withChannelPredictionProgressString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.prediction.progress')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    def test_fromStr_withChannelCheerString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.cheer')
        assert result is TwitchWebsocketSubscriptionType.CHEER

    def test_fromStr_withChannelFollowString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.follow')
        assert result is TwitchWebsocketSubscriptionType.FOLLOW

    def test_fromStr_withChannelRaidString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.raid')
        assert result is TwitchWebsocketSubscriptionType.RAID

    def test_fromStr_withChannelSubscribeString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.subscribe')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIBE

    def test_fromStr_withChannelSubscriptionGiftString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.subscription.gift')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT

    def test_fromStr_withChannelSubscriptionMessageString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.subscription.message')
        assert result is TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    def test_fromStr_withChannelUpdateString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('channel.update')
        assert result is TwitchWebsocketSubscriptionType.CHANNEL_UPDATE

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketSubscriptionType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = TwitchWebsocketSubscriptionType.fromStr(None)
        assert result is None

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketSubscriptionType.fromStr(' ')
        assert result is None

    def test_getVersion_withChannelPointsRedemption(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollBegin(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollEnd(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_END.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollProgress(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionBegin(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionEnd(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionLock(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionProgress(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS.getVersion()
        assert version == '1'

    def test_getVersion_withChannelUpdate(self):
        version = TwitchWebsocketSubscriptionType.CHANNEL_UPDATE.getVersion()
        assert version == '2'

    def test_getVersion_withCheer(self):
        version = TwitchWebsocketSubscriptionType.CHEER.getVersion()
        assert version == '1'

    def test_getVersion_withFollow(self):
        version = TwitchWebsocketSubscriptionType.FOLLOW.getVersion()
        assert version == '2'

    def test_getVersion_withRaid(self):
        version = TwitchWebsocketSubscriptionType.RAID.getVersion()
        assert version == '1'

    def test_getVersion_withSubscribe(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIBE.getVersion()
        assert version == '1'

    def test_getVersion_withSubscriptionGift(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT.getVersion()
        assert version == '1'

    def test_getVersion_withSubscriptionMessage(self):
        version = TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE.getVersion()
        assert version == '1'

    def test_toStr_withChannelPointsRedemption(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION.toStr()
        assert string == 'channel.channel_points_custom_reward_redemption.add'

    def test_toStr_withChannelPollBegin(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_POLL_BEGIN.toStr()
        assert string == 'channel.poll.begin'

    def test_toStr_withChannelPollEnd(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_POLL_END.toStr()
        assert string == 'channel.poll.end'

    def test_toStr_withChannelPollProgress(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_POLL_PROGRESS.toStr()
        assert string == 'channel.poll.progress'

    def test_toStr_withChannelPredictionBegin(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN.toStr()
        assert string == 'channel.prediction.begin'

    def test_toStr_withChannelPredictionEnd(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END.toStr()
        assert string == 'channel.prediction.end'

    def test_toStr_withChannelPredictionLock(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK.toStr()
        assert string == 'channel.prediction.lock'

    def test_toStr_withChannelPredictionProgress(self):
        string = TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS.toStr()
        assert string == 'channel.prediction.progress'

    def test_toStr_withCheer(self):
        string = TwitchWebsocketSubscriptionType.CHEER.toStr()
        assert string == 'channel.cheer'

    def test_toStr_withFollow(self):
        string = TwitchWebsocketSubscriptionType.FOLLOW.toStr()
        assert string == 'channel.follow'

    def test_toStr_withRaid(self):
        string = TwitchWebsocketSubscriptionType.RAID.toStr()
        assert string == 'channel.raid'

    def  test_toStr_withSubscribe(self):
        string = TwitchWebsocketSubscriptionType.SUBSCRIBE.toStr()
        assert string == 'channel.subscribe'

    def test_toStr_withSubscriptionGift(self):
        string = TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT.toStr()
        assert string == 'channel.subscription.gift'

    def test_toStr_withSubscriptionMessage(self):
        string = TwitchWebsocketSubscriptionType.SUBSCRIPTION_MESSAGE.toStr()
        assert string == 'channel.subscription.message'
