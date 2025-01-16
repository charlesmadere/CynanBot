from typing import Any

from frozendict import frozendict

from src.users.timeout.timeoutBoosterPack import TimeoutBoosterPack
from src.users.timeout.timeoutBoosterPackJsonParser import TimeoutBoosterPackJsonParser
from src.users.timeout.timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from src.users.timeout.timeoutBoosterPackType import TimeoutBoosterPackType


class TestTimoutBoosterPackJsonParser:

    jsonParser: TimeoutBoosterPackJsonParserInterface = TimeoutBoosterPackJsonParser()

    def test_parseBoosterPack1(self):
        jsonContents: dict[str, Any] = {
            'durationSeconds': 60,
            'rewardId': 'abc123'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, TimeoutBoosterPack)
        assert result.randomChanceEnabled
        assert result.durationSeconds == 60
        assert result.rewardId == 'abc123'

    def test_parseBoosterPack2(self):
        jsonContents: dict[str, Any] = {
            'durationSeconds': 120,
            'randomChanceEnabled': False,
            'rewardId': 'def456'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, TimeoutBoosterPack)
        assert not result.randomChanceEnabled
        assert result.durationSeconds == 120
        assert result.rewardId == 'def456'

    def test_parseBoosterPack3(self):
        jsonContents: dict[str, Any] = {
            'durationSeconds': 300,
            'randomChanceEnabled': True,
            'rewardId': 'xyz789'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, TimeoutBoosterPack)
        assert result.randomChanceEnabled
        assert result.durationSeconds == 300
        assert result.rewardId == 'xyz789'

    def test_parseBoosterPack4(self):
        jsonContents: dict[str, Any] = {
            'durationSeconds': 30,
            'randomChanceEnabled': True,
            'rewardId': 'lolomg',
            'timeoutType': 'random'
        }

        result = self.jsonParser.parseBoosterPack(jsonContents)
        assert isinstance(result, TimeoutBoosterPack)
        assert result.randomChanceEnabled
        assert result.durationSeconds == 30
        assert result.rewardId == 'lolomg'
        assert result.timeoutType is TimeoutBoosterPackType.RANDOM_TARGET

    def test_parseBoosterPackType_withRandomString(self):
        result = self.jsonParser.parseBoosterPackType('random')
        assert result is TimeoutBoosterPackType.RANDOM_TARGET

    def test_parseBoosterPackType_withUserString(self):
        result = self.jsonParser.parseBoosterPackType('user')
        assert result is TimeoutBoosterPackType.USER_TARGET

    def test_parseBoosterPacks(self):
        jsonContents: list[dict[str, Any]] = [
            {
                'durationSeconds': 120,
                'randomChanceEnabled': False,
                'rewardId': 'def456'
            },
            {
                'durationSeconds': 60,
                'rewardId': 'abc123'
            },
            {
               'durationSeconds': 300,
                'randomChanceEnabled': True,
                'rewardId': 'xyz789'
            }
        ]

        result = self.jsonParser.parseBoosterPacks(jsonContents)
        assert isinstance(result, frozendict)
        assert len(result) == 3

        boosterPack = result.get('def456')
        assert isinstance(boosterPack, TimeoutBoosterPack)
        assert boosterPack.durationSeconds == 120
        assert not boosterPack.randomChanceEnabled
        assert boosterPack.rewardId == 'def456'

        boosterPack = result.get('abc123')
        assert isinstance(boosterPack, TimeoutBoosterPack)
        assert boosterPack.durationSeconds == 60
        assert boosterPack.randomChanceEnabled
        assert boosterPack.rewardId == 'abc123'

        boosterPack = result.get('xyz789')
        assert isinstance(boosterPack, TimeoutBoosterPack)
        assert boosterPack.durationSeconds == 300
        assert boosterPack.randomChanceEnabled
        assert boosterPack.rewardId == 'xyz789'

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.jsonParser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.jsonParser.parseBoosterPacks(None)
        assert result is None
