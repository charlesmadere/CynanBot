import pytest

from frozendict import frozendict

from src.users.supStreamer.supStreamerBoosterPack import SupStreamerBoosterPack
from src.users.supStreamer.supStreamerBoosterPackJsonParserInterface import SupStreamerBoosterPackJsonParserInterface
from src.users.supStreamer.supStreamerBoosterPackJsonParser import SupStreamerBoosterPackJsonParser

class TestSupStreamerBoosterPackJsonParser:

    supStreamerBoosterPackJsonParser: SupStreamerBoosterPackJsonParserInterface = SupStreamerBoosterPackJsonParser()

    def test_parseBoosterPack(self):
        boosterPack = SupStreamerBoosterPack(
            message = "test",
            reply = "ahoy"
        )

        result = self.supStreamerBoosterPackJsonParser.parseBoosterPack({
            'message': boosterPack.directoryPath,
            'reply': boosterPack.isImmediate
        })

        assert isinstance(result, SupStreamerBoosterPack)
        assert result == boosterPack
        assert result.message == boosterPack.message
        assert result.reply == boosterPack.reply

    def test_parseRedemption_withEmptyDictionary(self):
        result: SupStreamerBoosterPack | None = None

        with pytest.raises(Exception):
            self.supStreamerBoosterPackJsonParser.parseBoosterPack(dict())

        assert result is None

    def test_parseRedemption_withNone(self):
        result: SupStreamerBoosterPack | None = None

        with pytest.raises(Exception):
            self.supStreamerBoosterPackJsonParser.parseBoosterPack(None) # type: ignore

        assert result is None

    def test_parseRedemptions(self):
        boosterPack1 = SupStreamerBoosterPack(
            message = "test",
            reply = "ahoy"
        )

        boosterPack2 = SupStreamerBoosterPack(
            message = "test2",
            reply = "ahoy2"
        )

        result = self.supStreamerBoosterPackJsonParser.parseBoosterPack([
            {
                'message': "test",
                'reply': "ahoy"
            },
            {
                'message': "test2",
                'reply': "ahoy2"
            }
        ])

        assert isinstance(result, frozendict)
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
