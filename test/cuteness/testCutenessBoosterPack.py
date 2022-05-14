import unittest

from CynanBotCommon.cuteness.cutenessBoosterPack import CutenessBoosterPack


class TestCutenessBoosterPack(unittest.TestCase):

    def test_getAmount(self):
        boosterPack = CutenessBoosterPack(1, "rewardId")
        self.assertEqual(1, boosterPack.getAmount())

        boosterPack = CutenessBoosterPack(2, "rewardId")
        self.assertEqual(2, boosterPack.getAmount())

        boosterPack = CutenessBoosterPack(-1, "rewardId")
        self.assertEqual(-1, boosterPack.getAmount())

    def test_getRewardId(self):
        boosterPack = CutenessBoosterPack(1, "Samus")
        self.assertEqual("Samus", boosterPack.getRewardId())

        boosterPack = CutenessBoosterPack(2, "Mario")
        self.assertEqual("Mario", boosterPack.getRewardId())

        boosterPack = CutenessBoosterPack(-1, "Link")
        self.assertEqual("Link", boosterPack.getRewardId())
