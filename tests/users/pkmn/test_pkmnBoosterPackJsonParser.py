import pytest
from frozendict import frozendict

from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.users.pkmn.pkmnBoosterPackJsonParser import PkmnBoosterPackJsonParser
from src.users.pkmn.pkmnBoosterPackJsonParserInterface import PkmnBoosterPackJsonParserInterface
from src.users.pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from src.users.pkmn.pkmnCatchType import PkmnCatchType


class TestPkmnBoosterPackJsonParser:

    timber: TimberInterface = TimberStub()

    jsonParser: PkmnBoosterPackJsonParserInterface = PkmnBoosterPackJsonParser(
        timber = timber
    )

    def test_parseBoosterPack1(self):
        rewardId = 'abc123'

        boosterPack = self.jsonParser.parseBoosterPack({
            'rewardId': rewardId
        })

        assert isinstance(boosterPack, PkmnCatchBoosterPack)
        assert boosterPack.catchType is None
        assert boosterPack.rewardId == rewardId

    def test_parseBoosterPack2(self):
        rewardId = 'def456'

        boosterPack = self.jsonParser.parseBoosterPack({
            'catchType': 'normal',
            'rewardId': rewardId
        })

        assert isinstance(boosterPack, PkmnCatchBoosterPack)
        assert boosterPack.catchType is PkmnCatchType.NORMAL
        assert boosterPack.rewardId == rewardId

    def test_parseBoosterPack_withEmptyDictionary(self):
        boosterPack: PkmnCatchBoosterPack | None = None

        with pytest.raises(Exception):
            boosterPack = self.jsonParser.parseBoosterPack(dict())

        assert boosterPack is None

    def test_parseBoosterPack_withNone(self):
        boosterPack: PkmnCatchBoosterPack | None = None

        with pytest.raises(Exception):
            boosterPack = self.jsonParser.parseBoosterPack(None) # type: ignore

        assert boosterPack is None

    def test_parseBoosterPacks(self):
        rewardId1 = 'abc123'
        rewardId2 = 'def456'
        rewardId3 = 'xyz789'

        boosterPacks = self.jsonParser.parseBoosterPacks([
            {
                'catchType': 'normal',
                'rewardId': rewardId1
            },
            {
                'catchType': 'great',
                'rewardId': rewardId2
            },
            {
                'catchType': 'ultra',
                'rewardId': rewardId3
            }
        ])

        assert isinstance(boosterPacks, frozendict)
        assert len(boosterPacks) == 3

        boosterPack = boosterPacks.get(rewardId1, None)
        assert isinstance(boosterPack, PkmnCatchBoosterPack)
        assert boosterPack.catchType is PkmnCatchType.NORMAL
        assert boosterPack.rewardId == rewardId1

        boosterPack = boosterPacks.get(rewardId2, None)
        assert isinstance(boosterPack, PkmnCatchBoosterPack)
        assert boosterPack.catchType is PkmnCatchType.GREAT
        assert boosterPack.rewardId == rewardId2

        boosterPack = boosterPacks.get(rewardId3, None)
        assert isinstance(boosterPack, PkmnCatchBoosterPack)
        assert boosterPack.catchType is PkmnCatchType.ULTRA
        assert boosterPack.rewardId == rewardId3

    def test_parseBoosterPacks_withEmptyList(self):
        boosterPacks = self.jsonParser.parseBoosterPacks(list())
        assert boosterPacks is None

    def test_parseBoosterPacks_withNone(self):
        boosterPacks = self.jsonParser.parseBoosterPacks(None)
        assert boosterPacks is None

    def test_parseCatchType_withEmptyString(self):
        catchType = self.jsonParser.parseCatchType('')
        assert catchType is None

    def test_parseCatchType_withGreatString(self):
        catchType = self.jsonParser.parseCatchType('great')
        assert catchType is PkmnCatchType.GREAT

    def test_parseCatchType_withNone(self):
        catchType = self.jsonParser.parseCatchType(None)
        assert catchType is None

    def test_parseCatchType_withNormalString(self):
        catchType = self.jsonParser.parseCatchType('normal')
        assert catchType is PkmnCatchType.NORMAL

    def test_parseCatchType_withUltraString(self):
        catchType = self.jsonParser.parseCatchType('ultra')
        assert catchType is PkmnCatchType.ULTRA

    def test_parseCatchType_withWhitespaceString(self):
        catchType = self.jsonParser.parseCatchType(' ')
        assert catchType is None
