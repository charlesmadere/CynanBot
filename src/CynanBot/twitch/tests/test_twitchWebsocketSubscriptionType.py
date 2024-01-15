from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TestTwitchWebsocketSubscriptionType():

    def test_fromStr_withChannelChannelPointsCustomRewardRedemptionString(self):
        result = WebsocketSubscriptionType.fromStr('channel.channel_points_custom_reward_redemption.add')
        assert result is WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION

    def test_fromStr_withChannelPollBeginString(self):
        result = WebsocketSubscriptionType.fromStr('channel.poll.begin')
        assert result is WebsocketSubscriptionType.CHANNEL_POLL_BEGIN

    def test_fromStr_withChannelPollEndString(self):
        result = WebsocketSubscriptionType.fromStr('channel.poll.end')
        assert result is WebsocketSubscriptionType.CHANNEL_POLL_END

    def test_fromStr_withChannelPollProgressString(self):
        result = WebsocketSubscriptionType.fromStr('channel.poll.progress')
        assert result is WebsocketSubscriptionType.CHANNEL_POLL_PROGRESS

    def test_fromStr_withChannelPredictionBeginString(self):
        result = WebsocketSubscriptionType.fromStr('channel.prediction.begin')
        assert result is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN

    def test_fromStr_withChannelPredictionEndString(self):
        result = WebsocketSubscriptionType.fromStr('channel.prediction.end')
        assert result is WebsocketSubscriptionType.CHANNEL_PREDICTION_END

    def test_fromStr_withChannelPredictionLockString(self):
        result = WebsocketSubscriptionType.fromStr('channel.prediction.lock')
        assert result is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK

    def test_fromStr_withChannelPredictionProgressString(self):
        result = WebsocketSubscriptionType.fromStr('channel.prediction.progress')
        assert result is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS

    def test_fromStr_withChannelCheerString(self):
        result = WebsocketSubscriptionType.fromStr('channel.cheer')
        assert result is WebsocketSubscriptionType.CHEER

    def test_fromStr_withChannelFollowString(self):
        result = WebsocketSubscriptionType.fromStr('channel.follow')
        assert result is WebsocketSubscriptionType.FOLLOW

    def test_fromStr_withChannelRaidString(self):
        result = WebsocketSubscriptionType.fromStr('channel.raid')
        assert result is WebsocketSubscriptionType.RAID

    def test_fromStr_withChannelSubscribeString(self):
        result = WebsocketSubscriptionType.fromStr('channel.subscribe')
        assert result is WebsocketSubscriptionType.SUBSCRIBE

    def test_fromStr_withChannelSubscriptionGiftString(self):
        result = WebsocketSubscriptionType.fromStr('channel.subscription.gift')
        assert result is WebsocketSubscriptionType.SUBSCRIPTION_GIFT

    def test_fromStr_withChannelSubscriptionMessageString(self):
        result = WebsocketSubscriptionType.fromStr('channel.subscription.message')
        assert result is WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE

    def test_fromStr_withChannelUpdateString(self):
        result = WebsocketSubscriptionType.fromStr('channel.update')
        assert result is WebsocketSubscriptionType.CHANNEL_UPDATE

    def test_fromStr_withEmptyString(self):
        result = WebsocketSubscriptionType.fromStr('')
        assert result is None

    def test_fromStr_withNone(self):
        result = WebsocketSubscriptionType.fromStr(None)
        assert result is None

    def test_fromStr_withWhitespaceString(self):
        result = WebsocketSubscriptionType.fromStr(' ')
        assert result is None

    def test_getVersion_withChannelPointsRedemption(self):
        version = WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollBegin(self):
        version = WebsocketSubscriptionType.CHANNEL_POLL_BEGIN.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollEnd(self):
        version = WebsocketSubscriptionType.CHANNEL_POLL_END.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPollProgress(self):
        version = WebsocketSubscriptionType.CHANNEL_POLL_PROGRESS.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionBegin(self):
        version = WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionEnd(self):
        version = WebsocketSubscriptionType.CHANNEL_PREDICTION_END.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionLock(self):
        version = WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK.getVersion()
        assert version == '1'

    def test_getVersion_withChannelPredictionProgress(self):
        version = WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS.getVersion()
        assert version == '1'

    def test_getVersion_withChannelUpdate(self):
        version = WebsocketSubscriptionType.CHANNEL_UPDATE.getVersion()
        assert version == '2'

    def test_getVersion_withCheer(self):
        version = WebsocketSubscriptionType.CHEER.getVersion()
        assert version == '1'

    def test_getVersion_withFollow(self):
        version = WebsocketSubscriptionType.FOLLOW.getVersion()
        assert version == '2'

    def test_getVersion_withRaid(self):
        version = WebsocketSubscriptionType.RAID.getVersion()
        assert version == '1'

    def test_getVersion_withSubscribe(self):
        version = WebsocketSubscriptionType.SUBSCRIBE.getVersion()
        assert version == '1'

    def test_getVersion_withSubscriptionGift(self):
        version = WebsocketSubscriptionType.SUBSCRIPTION_GIFT.getVersion()
        assert version == '1'

    def test_getVersion_withSubscriptionMessage(self):
        version = WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE.getVersion()
        assert version == '1'

    def test_toStr_withChannelPointsRedemption(self):
        string = WebsocketSubscriptionType.CHANNEL_POINTS_REDEMPTION.toStr()
        assert string == 'channel.channel_points_custom_reward_redemption.add'

    def test_toStr_withChannelPollBegin(self):
        string = WebsocketSubscriptionType.CHANNEL_POLL_BEGIN.toStr()
        assert string == 'channel.poll.begin'

    def test_toStr_withChannelPollEnd(self):
        string = WebsocketSubscriptionType.CHANNEL_POLL_END.toStr()
        assert string == 'channel.poll.end'

    def test_toStr_withChannelPollProgress(self):
        string = WebsocketSubscriptionType.CHANNEL_POLL_PROGRESS.toStr()
        assert string == 'channel.poll.progress'

    def test_toStr_withChannelPredictionBegin(self):
        string = WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN.toStr()
        assert string == 'channel.prediction.begin'

    def test_toStr_withChannelPredictionEnd(self):
        string = WebsocketSubscriptionType.CHANNEL_PREDICTION_END.toStr()
        assert string == 'channel.prediction.end'

    def test_toStr_withChannelPredictionLock(self):
        string = WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK.toStr()
        assert string == 'channel.prediction.lock'

    def test_toStr_withChannelPredictionProgress(self):
        string = WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS.toStr()
        assert string == 'channel.prediction.progress'

    def test_toStr_withCheer(self):
        string = WebsocketSubscriptionType.CHEER.toStr()
        assert string == 'channel.cheer'

    def test_toStr_withFollow(self):
        string = WebsocketSubscriptionType.FOLLOW.toStr()
        assert string == 'channel.follow'

    def test_toStr_withRaid(self):
        string = WebsocketSubscriptionType.RAID.toStr()
        assert string == 'channel.raid'

    def  test_toStr_withSubscribe(self):
        string = WebsocketSubscriptionType.SUBSCRIBE.toStr()
        assert string == 'channel.subscribe'

    def test_toStr_withSubscriptionGift(self):
        string = WebsocketSubscriptionType.SUBSCRIPTION_GIFT.toStr()
        assert string == 'channel.subscription.gift'

    def test_toStr_withSubscriptionMessage(self):
        string = WebsocketSubscriptionType.SUBSCRIPTION_MESSAGE.toStr()
        assert string == 'channel.subscription.message'
