from src.users.redemptionCounter.redemptionCounterBoosterPack import RedemptionCounterBoosterPack
from src.users.redemptionCounter.redemptionCounterBoosterPackParser import RedemptionCounterBoosterPackParser
from src.users.redemptionCounter.redemptionCounterBoosterPackParserInterface import \
    RedemptionCounterBoosterPackParserInterface


class TestRedemptionCounterBoosterPackParser:

    parser: RedemptionCounterBoosterPackParserInterface = RedemptionCounterBoosterPackParser()

    def test_parseBoosterPack(self):
        boosterPack = RedemptionCounterBoosterPack(
            incrementAmount = 3,
            counterName = 'CDs',
            emote = '💿',
            rewardId = 'abc123'
        )

        result = self.parser.parseBoosterPack({
            'incrementAmount': boosterPack.incrementAmount,
            'counterName': boosterPack.counterName,
            'emote': boosterPack.emote,
            'rewardId': boosterPack.rewardId
        })

        assert result.incrementAmount == boosterPack.incrementAmount
        assert result.counterName == boosterPack.counterName
        assert result.emote == boosterPack.emote
        assert result.rewardId == boosterPack.rewardId

    def test_parseBoosterPack_withoutIncrementAmount(self):
        boosterPack = RedemptionCounterBoosterPack(
            incrementAmount = 1,
            counterName = 'controllers',
            emote = '🎮',
            rewardId = 'xyz987'
        )

        result = self.parser.parseBoosterPack({
            'counterName': boosterPack.counterName,
            'emote': boosterPack.emote,
            'rewardId': boosterPack.rewardId
        })

        assert result.incrementAmount == boosterPack.incrementAmount
        assert result.counterName == boosterPack.counterName
        assert result.emote == boosterPack.emote
        assert result.rewardId == boosterPack.rewardId

    def test_parseBoosterPack_withoutEmote(self):
        boosterPack = RedemptionCounterBoosterPack(
            incrementAmount = 5,
            counterName = 'tickets',
            emote = None,
            rewardId = 'xyz987'
        )

        result = self.parser.parseBoosterPack({
            'incrementAmount': boosterPack.incrementAmount,
            'counterName': boosterPack.counterName,
            'rewardId': boosterPack.rewardId
        })

        assert result.incrementAmount == boosterPack.incrementAmount
        assert result.counterName == boosterPack.counterName
        assert result.emote == boosterPack.emote
        assert result.rewardId == boosterPack.rewardId

    def test_parseBoosterPack_withoutIncrementAmountOrEmote(self):
        boosterPack = RedemptionCounterBoosterPack(
            incrementAmount = 1,
            counterName = 'controllers',
            emote = None,
            rewardId = 'xyz987'
        )

        result = self.parser.parseBoosterPack({
            'counterName': boosterPack.counterName,
            'rewardId': boosterPack.rewardId
        })

        assert result.incrementAmount == boosterPack.incrementAmount
        assert result.counterName == boosterPack.counterName
        assert result.emote == boosterPack.emote
        assert result.rewardId == boosterPack.rewardId

    def test_parseBoosterPacks(self):
        boosterPack1 = RedemptionCounterBoosterPack(
            incrementAmount = 3,
            counterName = 'beans',
            emote = '🫘',
            rewardId = 'abc123'
        )

        boosterPack2 = RedemptionCounterBoosterPack(
            incrementAmount = 1,
            counterName = 'controllers',
            emote = None,
            rewardId = 'def456'
        )

        results = self.parser.parseBoosterPacks([
            {
                'incrementAmount': boosterPack1.incrementAmount,
                'counterName': boosterPack1.counterName,
                'emote': boosterPack1.emote,
                'rewardId': boosterPack1.rewardId
            },
            {
                'counterName': boosterPack2.counterName,
                'rewardId': boosterPack2.rewardId
            }
        ])

        assert results is not None
        assert len(results) == 2

        result = results[boosterPack1.rewardId]
        assert result.incrementAmount == boosterPack1.incrementAmount
        assert result.counterName == boosterPack1.counterName
        assert result.emote == boosterPack1.emote
        assert result.rewardId == boosterPack1.rewardId

        result = results[boosterPack2.rewardId]
        assert result.incrementAmount == boosterPack2.incrementAmount
        assert result.counterName == boosterPack2.counterName
        assert result.emote == boosterPack2.emote
        assert result.rewardId == boosterPack2.rewardId

    def test_parseBoosterPacks_withEmptyList(self):
        result = self.parser.parseBoosterPacks(list())
        assert result is None

    def test_parseBoosterPacks_withNone(self):
        result = self.parser.parseBoosterPacks(None)
        assert result is None

    def test_sanity(self):
        assert self.parser is not None
        assert isinstance(self.parser, RedemptionCounterBoosterPackParser)
        assert isinstance(self.parser, RedemptionCounterBoosterPackParserInterface)
