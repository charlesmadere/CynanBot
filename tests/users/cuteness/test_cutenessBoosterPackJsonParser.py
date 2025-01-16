from typing import Any

from frozendict import frozendict

from src.users.cuteness.cutenessBoosterPack import CutenessBoosterPack
from src.users.cuteness.cutenessBoosterPackJsonParser import CutenessBoosterPackJsonParser
from src.users.cuteness.cutenessBoosterPackJsonParserInterface import CutenessBoosterPackJsonParserInterface


class TestCutenessBoosterPackJsonParser:

    jsonParser: CutenessBoosterPackJsonParserInterface = CutenessBoosterPackJsonParser()

    def test_parseBoosterPack(self):
        jsonContents: dict[str, Any] = {
            'amount': 1,
            'rewardId': 'abc123'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, CutenessBoosterPack)
        assert result.amount == 1
        assert result.rewardId == 'abc123'

    def test_parseBoosterPacks(self):
        jsonContents: list[dict[str, Any]] = [
            {
                'amount': 25,
                'rewardId': 'def456'
            },
            {
                'amount': 1,
                'rewardId': 'abc123'
            }
        ]

        result = self.jsonParser.parseBoosterPacks(jsonContents)
        assert isinstance(result, frozendict)
        assert len(result) == 2

        boosterPack = result.get('def456')
        assert isinstance(boosterPack, CutenessBoosterPack)
        assert boosterPack.amount == 25
        assert boosterPack.rewardId == 'def456'

        boosterPack = result.get('abc123')
        assert isinstance(boosterPack, CutenessBoosterPack)
        assert boosterPack.amount == 1
        assert boosterPack.rewardId == 'abc123'

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.jsonParser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.jsonParser.parseBoosterPacks(None)
        assert result is None
