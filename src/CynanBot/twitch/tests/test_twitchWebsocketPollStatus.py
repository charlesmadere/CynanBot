from CynanBot.twitch.websocket.twitchWebsocketPollStatus import \
    TwitchWebsocketPollStatus


class TestTwitchWebsocketPollStatus():

    def test_fromStr_withActiveString(self):
        result = TwitchWebsocketPollStatus.fromStr('active')
        assert result is TwitchWebsocketPollStatus.ACTIVE

    def test_fromStr_withArchivedString(self):
        result = TwitchWebsocketPollStatus.fromStr('archived')
        assert result is TwitchWebsocketPollStatus.ARCHIVED

    def test_fromStr_withCompletedString(self):
        result = TwitchWebsocketPollStatus.fromStr('completed')
        assert result is TwitchWebsocketPollStatus.COMPLETED

    def test_fromStr_withEmptyString(self):
        result = TwitchWebsocketPollStatus.fromStr('')
        assert result is None

    def test_fromStr_withInvalidString(self):
        result = TwitchWebsocketPollStatus.fromStr('invalid')
        assert result is TwitchWebsocketPollStatus.INVALID

    def test_fromStr_withModeratedString(self):
        result = TwitchWebsocketPollStatus.fromStr('moderated')
        assert result is TwitchWebsocketPollStatus.MODERATED

    def test_fromStr_withNone(self):
        result = TwitchWebsocketPollStatus.fromStr(None)
        assert result is None

    def test_fromStr_withTerminatedString(self):
        result = TwitchWebsocketPollStatus.fromStr('terminated')
        assert result is TwitchWebsocketPollStatus.TERMINATED

    def test_fromStr_withWhitespaceString(self):
        result = TwitchWebsocketPollStatus.fromStr(' ')
        assert result is None
