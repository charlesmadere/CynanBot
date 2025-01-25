import pytest

from src.twitch.ircTagsParser.twitchIrcTagsParser import TwitchIrcTagsParser
from src.twitch.ircTagsParser.twitchIrcTagsParserInterface import TwitchIrcTagsParserInterface


class TestTwitchIrcTagsParser:

    parser: TwitchIrcTagsParserInterface = TwitchIrcTagsParser()

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, TwitchIrcTagsParser)
        assert isinstance(self.parser, TwitchIrcTagsParserInterface)
