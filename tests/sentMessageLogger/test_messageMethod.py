from src.sentMessageLogger.messageMethod import MessageMethod


class TestMessageMethod:

    def test_toStr(self):
        results: set[str] = set()

        for messageMethod in MessageMethod:
            results.add(messageMethod.toStr())

        assert len(results) == len(MessageMethod)

    def test_toStr_withIrc(self):
        result = MessageMethod.IRC.toStr()
        assert result == 'IRC'

    def test_toStr_withTwitchApi(self):
        result = MessageMethod.TWITCH_API.toStr()
        assert result == 'Twitch API'
