from typing import Optional

import pytest

from CynanBot.twitch.websocket.twitchWebsocketPollStatus import \
    TwitchWebsocketPollStatus


class TestTwitchWebsocketPollStatus():

    def test_fromStr_withArchivedString(self):
        result = TwitchWebsocketPollStatus.fromStr('archived')
        assert result is TwitchWebsocketPollStatus.ARCHIVED

    def test_fromStr_withCompletedString(self):
        result = TwitchWebsocketPollStatus.fromStr('completed')
        assert result is TwitchWebsocketPollStatus.COMPLETED

    def test_fromStr_withEmptyString(self):
        result: Optional[TwitchWebsocketPollStatus] = None

        with pytest.raises(Exception):
            result = TwitchWebsocketPollStatus.fromStr('')

        assert result is None

    def test_fromStr_withNone(self):
        result: Optional[TwitchWebsocketPollStatus] = None

        with pytest.raises(Exception):
            result = TwitchWebsocketPollStatus.fromStr(None)

        assert result is None

    def test_fromStr_withTerminatedString(self):
        result = TwitchWebsocketPollStatus.fromStr('terminated')
        assert result is TwitchWebsocketPollStatus.TERMINATED

    def test_fromStr_withWhitespaceString(self):
        result: Optional[TwitchWebsocketPollStatus] = None

        with pytest.raises(Exception):
            result = TwitchWebsocketPollStatus.fromStr(' ')

        assert result is None
