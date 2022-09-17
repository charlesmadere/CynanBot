import unittest

from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType


class TestPkmnCatchBoosterPack(unittest.TestCase):

    def test_getCatchType(self):
        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.NORMAL, "rewardId")
        self.assertEqual(PkmnCatchType.NORMAL, boosterPack.getCatchType())

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.GREAT, "rewardId")
        self.assertEqual(PkmnCatchType.GREAT, boosterPack.getCatchType())

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.ULTRA, "rewardId")
        self.assertEqual(PkmnCatchType.ULTRA, boosterPack.getCatchType())

    def test_getRewardId(self):
        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.NORMAL, "Samus")
        self.assertEqual("Samus", boosterPack.getRewardId())

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.GREAT, "Mario")
        self.assertEqual("Mario", boosterPack.getRewardId())

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.ULTRA, "Link")
        self.assertEqual("Link", boosterPack.getRewardId())
