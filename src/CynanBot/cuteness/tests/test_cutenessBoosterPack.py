from CynanBot.cuteness.cutenessBoosterPack import CutenessBoosterPack


class TestCutenessBoosterPack():

    def test_getAmount(self):
        boosterPack = CutenessBoosterPack(1, 'rewardId')
        assert 1 == boosterPack.getAmount()

        boosterPack = CutenessBoosterPack(2, 'rewardId')
        assert 2 == boosterPack.getAmount()

        boosterPack = CutenessBoosterPack(-1, 'rewardId')
        assert -1 == boosterPack.getAmount()

    def test_getRewardId(self):
        boosterPack = CutenessBoosterPack(1, 'Samus')
        assert 'Samus' == boosterPack.getRewardId()

        boosterPack = CutenessBoosterPack(2, 'Mario')
        assert 'Mario' == boosterPack.getRewardId()

        boosterPack = CutenessBoosterPack(-1, 'Link')
        assert 'Link' == boosterPack.getRewardId()
