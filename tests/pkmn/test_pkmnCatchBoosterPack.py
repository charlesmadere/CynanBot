from pkmn.pkmnCatchBoosterPack import PkmnCatchBoosterPack
from pkmn.pkmnCatchType import PkmnCatchType


class TestPkmnCatchBoosterPack():

    def test_getCatchType(self):
        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.NORMAL, "rewardId")
        assert boosterPack.getCatchType() == PkmnCatchType.NORMAL

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.GREAT, "rewardId")
        assert boosterPack.getCatchType() == PkmnCatchType.GREAT

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.ULTRA, "rewardId")
        assert boosterPack.getCatchType() == PkmnCatchType.ULTRA

    def test_getRewardId(self):
        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.NORMAL, "Samus")
        assert boosterPack.getRewardId() == "Samus"

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.GREAT, "Mario")
        assert boosterPack.getRewardId() == "Mario"

        boosterPack = PkmnCatchBoosterPack(PkmnCatchType.ULTRA, "Link")
        assert boosterPack.getRewardId() == "Link"
