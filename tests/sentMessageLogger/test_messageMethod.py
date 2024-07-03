from src.sentMessageLogger.messageMethod import MessageMethod


class TestMessageMethod():

    def test_toStr_withIrc(self):
        result = MessageMethod.IRC.toStr()
        assert result == 'IRC'

    def test_toStr_withTwitchApi(self):
        result = MessageMethod.TWITCH_API.toStr()
        assert result == 'Twitch API'
