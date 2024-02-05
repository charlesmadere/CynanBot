from CynanBot.twitch.api.twitchPollStatus import TwitchPollStatus


class TestTwitchWebsocketPollStatus():

    def test_fromStr_withActiveString(self):
        result = TwitchPollStatus.fromStr('active')
        assert result is TwitchPollStatus.ACTIVE

    def test_fromStr_withArchivedString(self):
        result = TwitchPollStatus.fromStr('archived')
        assert result is TwitchPollStatus.ARCHIVED

    def test_fromStr_withCompletedString(self):
        result = TwitchPollStatus.fromStr('completed')
        assert result is TwitchPollStatus.COMPLETED

    def test_fromStr_withEmptyString(self):
        result = TwitchPollStatus.fromStr('')
        assert result is None

    def test_fromStr_withInvalidString(self):
        result = TwitchPollStatus.fromStr('invalid')
        assert result is TwitchPollStatus.INVALID

    def test_fromStr_withModeratedString(self):
        result = TwitchPollStatus.fromStr('moderated')
        assert result is TwitchPollStatus.MODERATED

    def test_fromStr_withNone(self):
        result = TwitchPollStatus.fromStr(None)
        assert result is None

    def test_fromStr_withTerminatedString(self):
        result = TwitchPollStatus.fromStr('terminated')
        assert result is TwitchPollStatus.TERMINATED

    def test_fromStr_withWhitespaceString(self):
        result = TwitchPollStatus.fromStr(' ')
        assert result is None
