from typing import Optional

from CynanBot.twitch.websocket.websocketOutcomeColor import \
    WebsocketOutcomeColor


class TestTwitchWebsocketOutcomeColor():

    def test_fromStr_withBlueString(self):
        result = WebsocketOutcomeColor.fromStr('blue')
        assert result is WebsocketOutcomeColor.BLUE

    def test_fromStr_withEmptyString(self):
        result: Optional[WebsocketOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketOutcomeColor.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withNone(self):
        result: Optional[WebsocketOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketOutcomeColor.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromStr_withPinkString(self):
        result = WebsocketOutcomeColor.fromStr('pink')
        assert result is WebsocketOutcomeColor.PINK

    def test_fromStr_withWhitespaceString(self):
        result: Optional[WebsocketOutcomeColor] = None
        exception: Optional[Exception] = None

        try:
            result = WebsocketOutcomeColor.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)
