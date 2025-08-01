from src.chatterInventory.models.chatterItemType import ChatterItemType


class TestChatterItemType:

    def test_humanName_withAll(self):
        results: set[str] = set()

        for itemType in ChatterItemType:
            results.add(itemType.humanName)

        assert len(results) == len(ChatterItemType)

    def test_humanName_withAirStrike(self):
        result = ChatterItemType.AIR_STRIKE.humanName
        assert result == 'Air Strike'

    def test_humanName_withBanana(self):
        result = ChatterItemType.BANANA.humanName
        assert result == 'Banana'

    def test_humanName_withGrenade(self):
        result = ChatterItemType.GRENADE.humanName
        assert result == 'Grenade'
