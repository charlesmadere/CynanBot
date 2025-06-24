import pytest
from frozenlist import FrozenList

from src.users.supStreamer.supStreamerBoosterPack import SupStreamerBoosterPack
from src.users.supStreamer.supStreamerBoosterPackJsonParser import SupStreamerBoosterPackJsonParser
from src.users.supStreamer.supStreamerBoosterPackJsonParserInterface import SupStreamerBoosterPackJsonParserInterface


class TestSupStreamerBoosterPackJsonParser:

    parser: SupStreamerBoosterPackJsonParserInterface = SupStreamerBoosterPackJsonParser()

    def test_parseBoosterPack(self):
        boosterPack = SupStreamerBoosterPack(
            message = "test",
            reply = "ahoy"
        )

        result = self.parser.parseBoosterPack({
            'message': boosterPack.message,
            'reply': boosterPack.reply
        })

        assert isinstance(result, SupStreamerBoosterPack)
        assert result == boosterPack
        assert result.message == boosterPack.message
        assert result.reply == boosterPack.reply

    def test_parseBoosterPack_withEmptyDictionary(self):
        result: SupStreamerBoosterPack | None = None

        with pytest.raises(Exception):
            result = self.parser.parseBoosterPack(dict())

        assert result is None

    def test_parseBoosterPack_withNone(self):
        result: SupStreamerBoosterPack | None = None

        with pytest.raises(Exception):
            result = self.parser.parseBoosterPack(None) # type: ignore

        assert result is None

    def test_parseBoosterPacks(self):
        boosterPack1 = SupStreamerBoosterPack(
            message = "test",
            reply = "ahoy"
        )

        boosterPack2 = SupStreamerBoosterPack(
            message = "test2",
            reply = "ahoy2"
        )

        result = self.parser.parseBoosterPacks([
            {
                'message': "test",
                'reply': "ahoy"
            },
            {
                'message': "test2",
                'reply': "ahoy2"
            }
        ])

        assert isinstance(result, FrozenList)
        assert len(result) == 2


        redemption = result[0]
        assert isinstance(redemption, SupStreamerBoosterPack)
        assert redemption == boosterPack1
        assert redemption.message == boosterPack1.message
        assert redemption.reply == boosterPack1.reply

        redemption = result[1]
        assert isinstance(redemption, SupStreamerBoosterPack)
        assert redemption == boosterPack2
        assert redemption.message == boosterPack2.message
        assert redemption.reply == boosterPack2.reply

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.parser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.parser.parseBoosterPacks(None)
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, SupStreamerBoosterPackJsonParser)
        assert isinstance(self.parser, SupStreamerBoosterPackJsonParserInterface)
